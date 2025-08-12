from abc import abstractmethod
from mag_scripts.logger import logger


class MetaBase:
    # Registry of actions and their name and description.
    _registry : dict[str,'MetaBase'] = {}
    _topic_registry : dict[str,list[str]] = {}
    name : str
    description : str
    topic : list = []

    # Registration behavior
    def __init_subclass__(cls,**kw):
        super().__init_subclass__(**kw)
        name = getattr(cls,'name', None)
        cls.set_topic(cls.topic)
        # Checker
        if not name or not isinstance(name, str) or len(name) < 1:  
            raise TypeError(
                f'{cls.__name__} Must define a non-empty string class attribute "name"'
                )
        if name in MetaBase._registry:
            raise TypeError(f'"name"{name} already exists')
        cls._registry[cls.name] = cls
        cls._topic_registry[cls.name] = cls.topic
        logger.info(f'{cls.name} was registered')   
        logger.info(f'{cls.name} Topics: {cls.topic}') 
    @abstractmethod
    def check(self,ctx: dict) -> bool:
       ...

    @abstractmethod
    def execute(self):
        ...
    # TODO: 完成Monika演出的功能
    @classmethod
    def set_topic(cls, ctx: list):
        MetaBase.topic = ctx
# Init the registry
MetaBase._registry = {}
        
    
        