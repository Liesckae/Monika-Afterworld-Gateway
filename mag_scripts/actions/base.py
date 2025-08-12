from abc import abstractmethod
from mag_scripts.logger import logger

class MetaBase:
    # Registry of actions and their name and description.
    _registry : dict[str,'MetaBase'] = {}
    _script_registry : dict[str,list[str]] = {}
    name : str
    description : str
    script : list = []

    # Registration behavior
    def __init_subclass__(cls,**kw):
        super().__init_subclass__(**kw)
        name = getattr(cls,'name', None)
        cls.set_script(cls.script)
        # Checker
        if not name or not isinstance(name, str) or len(name) < 1:  
            raise TypeError(
                f'{cls.__name__} Must define a non-empty string class attribute "name"'
                )
        if name in MetaBase._registry:
            raise TypeError(f'"name"{name} already exists')
        cls._registry[cls.name] = cls
        cls._script_registry[cls.name] = cls.script
        logger.info(f'{cls.name} was registered')   
        logger.info(f'{cls.name} Script: {cls.script}') 
    @abstractmethod
    def check(self,ctx: dict) -> bool:
       ...

    @abstractmethod
    def execute(self):
        ...
    # TODO: 完成Monika演出的功能
    @classmethod
    def set_script(cls, ctx: list):
        if not ctx:
            MetaBase.script = [cls.name.lower() + '.rpy']
        else:
            MetaBase.script = ctx
# Init the registry
MetaBase._registry = {}
        
    
        