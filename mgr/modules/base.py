import utils

m_logger = utils.get_default_logger()

class BaseMeta(type):
    # Base的元类，当Base的子类被定义时实例化一个对象，并加载到注册表
    def __new__(cls, clsname, bases, clsdict):
        new_cls = super().__new__(cls, clsname, bases, clsdict)
        module_instance = new_cls()
        return new_cls
        

class Base:
    # Base类本身没什么可写的，只需要继承这个类即可，具体怎么实现看各个子模块怎么写
    __metaclass__ = BaseMeta
    
    name = ""
    desc = ""
    tags = []
    topics = []
    triggers = []       # 触发器列表，当所有触发器的check方法都返回true时，将执行模块的执行入口，名字不是必填的，
                        # 但是为了能找到触发器，建议填写
    is_enable = True        # 默认启用
    
    def __init__(self):
        self.name = self.__class__.name
        self.desc = self.__class__.desc
        self.tags = self.__class__.tags
        self.topics = self.__class__.topics
        self.triggers = self.__class__.triggers
        self._args = None  # 存储传递给execute的参数
        # 把实例注册到注册表
        self._register()
    
    def execute(self):
        # 这是每个模块的执行入口，调用之前先把参数传递进来
        if self._args is not None:
            args, kwargs = self._args
            # 在这里执行模块逻辑，args和kwargs是传递的参数
            # 子类可以覆盖此方法以实现具体逻辑
            pass
    
    def _register(self):
        # 这个类会被子模块继承，用于将模块实例加载到注册表,同时跳过Base类本身。
        # 写在模块里的名字不要重复或者留空，否则将会导致该模块无法正常加载。
        if self.__class__ == Base:
            pass
        else:
            if self.name == "":
                m_logger.warning(f"Failed to register: {self.__class__}, no module name is set.")
                return None
            if self.name in utils.get_module_registry().keys():
                m_logger.warning(f"Failed to register: {self.__class__}, name has been used.")
                return None
            utils.get_module_registry()[self.name] = self
            utils.get_trigger_registry()[self.triggers] = self
            
    def pass_args(self, *args, **kwargs):
        # 存储传递给execute的参数
        self._args = (args, kwargs)