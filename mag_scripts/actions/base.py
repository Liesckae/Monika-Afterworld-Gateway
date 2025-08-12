from abc import ABCMeta, abstractmethod
from mag_scripts.logger import logger


class MetaBaseMeta(ABCMeta):
    def __init__(cls, name, bases, namespace):
        super(MetaBaseMeta, cls).__init__(name, bases, namespace)
        if name == 'MetaBase':
            return
        cls_name = getattr(cls, 'name', None)
        cls.set_topic(cls.topic)
        # Checker
        if not cls_name or not isinstance(cls_name, basestring) or len(cls_name) < 1:
            raise TypeError(
                u'%s Must define a non-empty string class attribute "name"' % cls.__name__
            )
        if cls_name in MetaBase._registry:
            raise TypeError(u'"name"%s already exists' % cls_name)
        MetaBase._registry[cls.name] = cls
        MetaBase._topic_registry[cls.name] = cls.topic
        logger.info(u'%s was registered' % cls.name)
        logger.info(u'%s Topics: %s' % (cls.name, cls.topic))


class MetaBase(object):
    __metaclass__ = MetaBaseMeta
    # Registry of actions and their name and description.
    _registry = {}
    _topic_registry = {}
    name = None
    description = None
    topic = []

    @abstractmethod
    def check(self, ctx):
        pass

    @abstractmethod
    def execute(self):
        pass

    # TODO: Complete the function of Monika's performance
    @classmethod
    def set_topic(cls, ctx):
        MetaBase.topic = ctx

# Init the registry
MetaBase._registry = {}