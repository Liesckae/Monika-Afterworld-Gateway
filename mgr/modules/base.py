# -*- coding: utf-8 -*-
from __future__ import print_function, unicode_literals
import utils
from datetime import datetime

m_logger = utils.get_default_logger()

class BaseMeta(type):
    # Base的元类，当Base的子类被定义时实例化一个对象，并加载到注册表
    def __new__(cls, clsname, bases, clsdict):
        new_cls = super().__new__(cls, clsname, bases, clsdict)
        if clsname != 'Base':
            inst = new_cls()
            inst._register()
        return new_cls
        

class Base:
    # Base类本身没什么可写的，只需要继承这个类即可，具体怎么实现看各个子模块怎么写
    __metaclass__ = BaseMeta
    
    name = ""
    desc = ""
    tags = None
    topics = None
    triggers = None     # 触发器列表，当所有触发器的check方法都返回true时，将执行模块的执行入口，名字不是必填的，
                        # 但是为了能找到触发器，建议填写
    is_enable = True        # 默认启用
    
    def __init__(self):
        self.name = self.__class__.name
        self.desc = self.__class__.desc
        self.tags = list(self.__class__.tags or [])
        self.topics = list(self.__class__.topics or [])
        self.triggers = list(self.__class__.triggers or [])
        self._args = None  # 存储传递给execute的参数
    
    def execute(self):
        # 这是每个模块的执行入口，调用之前先把参数传递进来
        pass
    
    def get_runtime_args(self):
        return (datetime.now,), {}
    
    def _register(self):
        # 这个类会被子模块继承，用于将模块实例加载到注册表,同时跳过Base类本身。
        # 写在模块里的名字不要重复或者留空，否则将会导致该模块无法正常加载。
        if self.__class__.name == 'Base':
            pass
        else:
            if self.name == "":
                raise ValueError('module: {} name must be defined.'.format(self.__class__.__name__))
            if self.name in utils.get_module_registry().keys():
                raise ValueError('module: {} name duplicate.'.format(self.name))

            utils.get_module_registry()[self.name] = self
            utils.get_trigger_registry()[self.name] = list(self.triggers)
            
            
            