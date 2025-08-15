# -*- coding: utf-8 -*-
from abc import abstractmethod
from src.utils.logger import m_logger
import src.utils.constants as constants

# class TriggerBaseMeta(type):
#     def __new__(mcls, name, bases, ns):
#         cls = super(TriggerBaseMeta, mcls).__new__(mcls, name, bases, ns)

#         if bases:
#             cls_name = ns.get('name')
#             if not cls_name or not isinstance(cls_name, str) or len(cls_name) < 1:
#                 m_logger.warning("'{}'is not a valid class. Class must be named. It's not a valid Trigger subclass.")
#                 raise TypeError("Attribute 'name' must be set.")
#             if cls_name in constants.TRIGGERS_REGISTRY:
#                 m_logger.warning("Trigger named '{}' already registered.".format(cls_name))
#                 raise TypeError("Not a valid class. Class name already used.")

#             constants.TRIGGERS_REGISTRY[cls_name] = cls
#             m_logger.info('Trigger <{}> successfully registered.'.format(cls_name))
#         return cls

class TriggerBase(object):
    
    _trigger_registry = constants.TRIGGERS_REGISTRY
    
    type = 'base trigger'
    
    def __init__(self, name, desc=''):
        """Initialize when the subclass is instantiates

        Args:
            name (str): The name of the instance
            desc (str, optional): Description of this instance. Defaults to ''.

        Raises:
            Exception: This name is used. Check it again.
        """
        self.name = name
        self.desc = desc
        if name in TriggerBase._trigger_registry:
            m_logger.warning("Trigger named '{}' already registered.".format(name))
            raise Exception("Not a valid trigger. Trigger name already used.")
        TriggerBase._trigger_registry.update({name: self})

        m_logger.info("name: {},type: {} registered successfully.".format(self.name, self.__class__))
    @abstractmethod
    def check(self, ctx):
        pass

    @abstractmethod
    def execute(self, ctx):
        m_logger.info("trigger was triggered: name - > {} | type-> {}".format(self.name, self.type))


    
class TriggerManager:
    
    def __init__(self):
        self.refresh_registry()

    def get_trigger_registry(self):
        """Get the available triggers dictionary

        Returns:
            dict{str: TriggerBase}: A dictionary which contains name as key, and module as value
        """
        return TriggerBase._trigger_registry
    
    def refresh_registry(self):
        self._registry = TriggerBase._trigger_registry
        