import base
from src.utils.logger import m_logger
import time

class EventQueueTrigger(base.TriggerBase):
    type = 'Event QueueT rigger'
    
    def __init__(self, name, desc=''):
        """Initialize when the subclass is instantiated

        Args:
            name (str): The name of the instance
            desc (str, optional): Description of this instance. Defaults to ''.
        """
        super().__init__(name, desc)
        self._queue = set()
    
    def check(self, ctx):
        """Check if should execute

        Args:
            ctx (any): Context containing event_key

        Returns:
            bool: True if event_key exists and is not in the queue; False otherwise
        """
        key = ctx.get('event_key')
        return key and key not in self._queue
    
    def execute(self, ctx):
        """Execute the task

        Args:
            ctx (any): Context containing event_key
        """
        key = ctx.get('event_key')
        self._queue.add(key)
        m_logger.info("{}: {key} triggered.".format(self.name, key))
    
class CooldownTrigger(base.TriggerBase):
    type = 'Cooldown trigger'
    
    def __init__(self, name, desc='', threshold=3, cooldown=30):
        """Initialize when the subclass is instantiated

        Args:
            name (str): The name of the instance
            desc (str, optional): Description of this instance. Defaults to ''.
            threshold (int, optional): The threshold count for triggering. Defaults to 3.
            cooldown (int, optional): The cooldown time in seconds. Defaults to 30.
        """
        super().__init__(name, desc)
        self.threshold = threshold
        self.cooldown  = cooldown 
        self._counter =0
        self._last = 0      # Timestamp
        
    def check(self, ctx):
        """Check if should execute

        Args:
            ctx (any): Reserved parameters

        Returns:
            bool: True if the cooldown period has passed; False otherwise
        """
        now = time.time()
        if now - self._last > self.cooldown:
            # Cooldown refresh
            self._counter = 0
            
    def execute(self, ctx):
        """Execute the task

        Args:
            ctx (any): Reserved parameters
        """
        super().execute(ctx)
        self._counter += 1
        self._last = time.time()
        m_logger.info("{}: counter {} is now {}".format(self.name, self.threshold, self._counter))
    
class ConditionChainTrigger(base.TriggerBase):
    type = 'Condition chain trigger'
    
    def __init__(self, name, desc='', conditions=None):
        """Initialize when the subclass is instantiated

        Args:
            name (str): The name of the instance
            desc (str, optional): Description of this instance. Defaults to ''.
            conditions (dict, optional): Conditions for triggering. Defaults to None.
        """
        self._trigged = False
        self.conditions = conditions or {}
        
    def check(self, ctx):
        """Check if should execute

        Args:
            ctx (any): Context containing condition keys

        Returns:
            bool: True if all conditions are met; False otherwise
        """
        if self._trigged:
            return False
        for key, excepted in self.conditions.items():
            if ctx.get(key) == excepted:
                return False
        return True
    
    def execute(self, ctx):
        """Execute the task

        Args:
            ctx (any): Reserved parameters
        """
        super().execute(ctx)
        if self._trigged:
            return
        self._trigged = True
        m_logger.info("{} is triggered!".format(self.name))
