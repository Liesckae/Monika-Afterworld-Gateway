from abc import ABCMeta, abstractmethod
from mag_scripts.logger import logger
from threading import Thread
import time
import subprocess
import random
import time
import pickle
import os
import sys

# Registry for module enable/disable status (persistent)
MODULE_STATUS_REGISTRY = {}
TRIGGER_REGISTRY = {}
MODULE_STATUS_FILE = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))),'module_status.pkl')

def load_module_status():
    """Load module status from file."""
    global MODULE_STATUS_REGISTRY
    if os.path.exists(MODULE_STATUS_FILE):
        try:
            with open(MODULE_STATUS_FILE, 'rb') as f:
                MODULE_STATUS_REGISTRY = pickle.load(f)
                logger.debug('Status was loaded.')
        except (EOFError, pickle.PickleError):
            MODULE_STATUS_REGISTRY = {}
            logger.warning('Failed to load module status; initializing empty registry.')
    else:
        MODULE_STATUS_REGISTRY = {}
        logger.debug('No module status file found; initializing empty registry.')

def save_module_status():
    """Save module status to file."""
    if not os.path.exists(MODULE_STATUS_FILE):
        f = open(MODULE_STATUS_FILE, 'wb')
        f.close()
    with open(MODULE_STATUS_FILE, 'wb') as f:
        pickle.dump(MODULE_STATUS_REGISTRY, f)
        logger.debug('Status was saved.')

class ModuleDaemon(Thread):
    """
    Lightweight daemon to monitor trigger conditions
    and activate modules when conditions are met
    """
    def __init__(self, triggers):
        Thread.__init__(self)
        self.daemon = True
        self.running = True
        self.triggers = triggers
    
    def run(self):
        """Main monitoring loop"""
        # TODO: Implementing multi-threaded concurrency detection
        
        while self.running:
            try:
                logger.debug('ModuleDaemon polling registry (running=%s)', self.running)
                for name, cls in MetaBase._registry.items():
                    logger.debug('Checking module: %s' % name)
                    
                    # DEBUG
                    MetaBase.enable_module('test')
                    
                    if MetaBase.is_module_enabled(name):
                        if cls.triggers:
                            # Ensure triggers is iterable
                            triggers = cls.triggers if isinstance(cls.triggers, (list, tuple)) else [cls.triggers]
                            logger.debug('Module %s has triggers: %s' % (name, triggers))
                            for trigger in triggers:
                                logger.debug('Checking trigger for module %s' % name)
                                if trigger(None).check(None):
                                    logger.debug('Trigger condition met for module %s, executing...' % name)
                                    cls.execute()
                                    logger.info(u'Module "%s" has been executed' % name)
                                    break
                                else:
                                    logger.debug('Trigger condition not met for module %s' % name)
                logger.debug('ModuleDaemon sleeping for 5 seconds')
                time.sleep(5)
                logger.debug('ModuleDaemon woke up')
            except Exception as e:
                logger.error(u'ModuleDaemon encountered an error: %s'%e)
                time.sleep(5) 
    
    def stop(self):
        self.running = False
    def set_triggers(self, triggers):
        self.triggers = triggers
        


class MetaBaseMeta(ABCMeta):
    def __init__(cls, name, bases, namespace):
        super(MetaBaseMeta, cls).__init__(name, bases, namespace)
        if name == 'MetaBase':
            return
        cls_name = getattr(cls, 'name', None)
        cls.set_topic(cls.topic)
        # Checker
        if not cls_name or not isinstance(cls_name, basestring) or len(cls_name) < 1:
            try:
                raise TypeError(
                    u'%s Must define a non-empty string class attribute "name"' % cls.__name__
                )
            except TypeError as e:
                logger.error("Error: {0}".format(e))
                raise
        if cls_name in MetaBase._registry:
            try:
                raise TypeError(u'"name"%s already exists' % cls_name)
            except TypeError as e:
                logger.error("Error: {0}".format(e))
                raise
        MetaBase._registry[cls.name] = cls
        MetaBase._topic_registry[cls.name] = cls.topic
        logger.info(u'%s was registered' % cls.name)
        logger.info(u'%s Topics: %s' % (cls.name, cls.topic))

class MetaBase(object):
    '''Base class for all actions'''
    __metaclass__ = MetaBaseMeta
    # Registry of actions and their name and description.
    _registry = {}
    _topic_registry = {}
    name = ""
    description = None
    topic = None
    triggers = None
    
    @classmethod
    def get_code_path(cls):
        mag_code_path = os.path.normpath(os.path.join(os.path.dirname(__file__), '..', '..','mag_code'))
        print('DEBUG: get_code_path() returned: %s' % mag_code_path)
        return mag_code_path

    @classmethod
    def enable_module(cls, module_name):
        """Enable a module and save status."""
        MODULE_STATUS_REGISTRY[module_name] = True
        save_module_status()

    @classmethod
    def disable_module(cls, module_name):
        """Disable a module and save status."""
        MODULE_STATUS_REGISTRY[module_name] = False
        save_module_status()

    @classmethod
    def is_module_enabled(cls, module_name):
        """Check if a module is enabled."""
        logger.debug('MODULE STATUS: %s' % MODULE_STATUS_REGISTRY)
        return MODULE_STATUS_REGISTRY.get(module_name, True)

    @classmethod
    def register_subclass(cls, subclass):
        if hasattr(subclass, 'triggers'):
            TRIGGER_REGISTRY[subclass.__name__] = subclass.triggers
            
    @classmethod
    def process(cls):
        '''Do something after execute method ends(Who knows what they will be doing)'''
        pass
    
    
    def execute(self):
        '''Default execution behaviour'''
        subprocess.Popen([sys.executable, self.code_path], stdout=sys.stdout, stderr=sys.stderr)
        logger.info("%s action executed" % self.name)
        

class TriggerBase:
    '''Trigger condition base class'''
    def __init__(self, trigger_id):
        self.trigger_id = trigger_id

    @abstractmethod
    def check(self, mas_ctx):
        """Check whether the trigger conditions are met
        Args:
            mas_ctx: MAS context object (must contain event, time, status and other data)
        """
        pass

class RandomTrigger(object):
    """
    Pure probability-based trigger (only for condition checking)
    Usage example:
        triggers = [RandomTrigger(0.1)]  # 10% trigger chance
    """
    def __init__(self, probability=0.1):
        self.probability = probability
    
    def check(self, ctx):
        """Check if trigger condition is met (no side effects)"""
        return random.random() < self.probability
    
class TimeTrigger(TriggerBase):
    '''Time-based trigger (uses in-game time)'''
    def __init__(self, start_hour, end_hour):
        self.start_hour = start_hour
        self.end_hour = end_hour

    def check(self, mas_ctx):
        return self.start_hour <= mas_ctx.current_hour < self.end_hour

class EventTrigger(TriggerBase):
    '''MAS event-based trigger'''
    def check(self, mas_ctx):
        return mas_ctx.event_mgr.is_triggered(self.trigger_id)
    
class DebugTrigger(TriggerBase):
    '''Return true when activated(I think this trigger is stupid but it's still useful)'''
    def check(self, mas_ctx):
        logger.debug(u'Module is triggered by DebugTrigger')
        return True

# Init the registry
MetaBase._registry = {}
load_module_status()