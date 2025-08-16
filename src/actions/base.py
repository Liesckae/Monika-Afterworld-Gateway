# -*- coding: utf-8 -*-
from abc import ABC, abstractmethod
from src.utils.logger import m_logger
import src.utils.file_ops as file_ops
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

class ActionBase(ABC):
    
    __metaclass__ = ActionBaseMeta
    
    _module_registry = {}
    
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
        self._module_registry = {}
        self.refresh_registry()
        
    def get_module_registry(self):
        """Get the available modules dictionary

        Returns:
            dict{str: Action}: A dictionary which contains name as key, and module as value
        """
        return ActionBase._module_registry
    
    def enable_module(self, module_name):
        """Enable a specific module in the registry

        Args:
            module_name (str): The name of the module

        Returns:
            bool: True if successful, false otherwise
        """
        if not module_name in ActionBase._module_registry:
            return False
        ActionBase._module_registry[module_name].is_abled = True
        return True
    
    def disable_module(self, module_name):
        """Disable a specific module in the registry

        Args:
            module_name (str): The name of the module

        Returns:
            bool: True if successful, false otherwise
        """
        if not module_name in ActionBase._module_registry:
            return False
        ActionBase._module_registry[module_name].is_abled = False
        return True
    
    def is_module_enabled(self, module_name):
        """Check if module is enable

        Args:
            module_name (name): The name of the module

        Returns:
            bool: Status of the module (True or False)
            None: If module_name is not found
        """
        if not module_name in ActionBase._module_registry:
            return None
        return ActionBase._module_registry[module_name].is_abled
    
    def remove_module(self, module_name):
        """Remove a specific module in the registry

        Args:
            module_name (str): The name of the module

        Returns:
            bool: True if successful, false otherwise
        """
        if not module_name in ActionBase._module_registry:
            return False
        ActionBase._module_registry.pop(module_name)
        return True
    
    def add_module(self, cls):
        """Add a new module in the registry

        Args:
            cls (ActionBase): The instance of the new module

        Returns:
            bool: True if operation is done without errors, and False otherwise.
        """
        if cls.name in ActionBase._module_registry:
            return False
        ActionBase._module_registry.update({cls.name: cls})
        return True
    
    def get_status(self):
        """get the status of the action
        
        Returns:
            dict: {str, bool} action status
        """
        return {cls.name: cls.is_abled() for name, cls in self._module_registry}
    
    def set_status(self, module_name, module_status):
        pass
        
    def refresh_registry(self):
        self._module_registry = file_ops.read_module_status()