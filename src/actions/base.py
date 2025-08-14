from abc import ABC, abstractmethod
from src.utils.logger import m_logger
import src.utils.constants as constants

class ActionBaseMeta(type):
    
    def __new__(mcls, name, bases, namespace):
        cls = super(ActionBaseMeta, mcls).__new__(mcls, name, bases, namespace)
        
        # Register 
        if bases:
            name_attr = namespace.get('name')
            if not name_attr or not isinstance(name_attr, str):
                m_logger.warning("'{}'is not a valid class. Class must be named. It's not a valid Action subclass.".format(name))
                raise Exception("Attribute 'name' must be set.")
            if name_attr in ActionBase._module_registry:
                m_logger.warning("Action named '{}' already registered".format(name_attr))
                raise Exception("Not a valid class. Class name already used.")
            
            ActionBase._module_registry.update({name_attr: cls})
            m_logger.info('Action <{}> successfully registered.'.format(name_attr))

            return cls

class ActionBase:
    
    __metaclass__ = ActionBaseMeta
    
    _module_registry = constants.MODULE_REGISTRY
    
    name = ''
    description = ''
    tags = []
    topics = []
    is_abled = False
    
    @abstractmethod
    def execute(self):
        pass
    
class ActionManager:

    def __init__(self):
        self.refresh_registry()
        
    def get_module_registry(self):
        """Get the available modules dictionary

        Returns:
            dict{str: ActionBase}: A dictionary which contains name as key, and module as value
        """
        return ActionBase._module_registry
    
    def enable_module(self, module_name):
        pass
    
    def disable_module(self, module_name):
        pass
    
    def is_module_enabled(self, module_name):
        pass
    
    def remove_module(self, module_name):
        pass
    
    def add_module(self, module):
        pass
    
    def refresh_registry(self):
        pass