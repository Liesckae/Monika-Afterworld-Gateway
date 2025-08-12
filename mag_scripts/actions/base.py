from abc import ABCMeta, abstractmethod
from mag_scripts.logger import logger


class MetaBase(object):
    __metaclass__ = ABCMeta
    # Registry of actions and their name and description.
    _registry = {}
    _topic_registry = {}
    name = None
    description = None
    topic = []

    # Registration behavior
    def __init_subclass__(cls, **kw):
        super(MetaBase, cls).__init_subclass__(** kw)
        name = getattr(cls, 'name', None)
        cls.set_topic(cls.topic)
        # Checker
        if not name or not isinstance(name, basestring) or len(name) < 1:  
            raise TypeError(
                u'%s Must define a non-empty string class attribute "name"' % cls.__name__
                )
        if name in MetaBase._registry:
            raise TypeError(u'"name"%s already exists' % name)
        cls._registry[cls.name] = cls
        cls._topic_registry[cls.name] = cls.topic
        logger.info(u'%s was registered' % cls.name)   
        logger.info(u'%s Topics: %s' % (cls.name, cls.topic)) 

    @abstractmethod
    def check(self, ctx):
        pass

    @abstractmethod
    def execute(self):
        pass

    # TODO: 完成Monika演出的功能
    @classmethod
    def set_topic(cls, ctx):
        MetaBase.topic = ctx

# Init the registry
MetaBase._registry = {}
        
    
        