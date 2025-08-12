class MetaBase(type):
    """
    Metaclass for module registration.
    """
    _registry = {}

    def __init__(cls, name, bases, namespace):
        super(MetaBase, cls).__init__(name, bases, namespace)
        if hasattr(cls, 'register_module'):
            cls.register_module(cls)