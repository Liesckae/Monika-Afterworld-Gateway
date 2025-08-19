# -*- coding: utf-8 -*-
# 模块基类，定义了模块的基本结构和注册逻辑
from datetime import datetime
import logging
import mgr.utils.constants as c



class BaseMeta(type):
    # 元类，用于自动注册模块
    def __new__(cls, clsname, bases, clsdict):
        new_cls = super(BaseMeta, cls).__new__(cls, clsname, bases, clsdict)
        if clsname != 'Base':
            inst = new_cls()
            inst._register()
        return new_cls
        

class Base(object):
    # 模块基类，所有模块应继承此类
    __metaclass__ = BaseMeta
    
    name = ""
    desc = ""
    tags = None
    topics = None
    triggers = None     # 触发器列表，当所有触发器的check方法都返回true时，将执行模块的执行入口，名字不是必填的，
                        # 但是为了能找到触发器，建议填写
    is_enable = True        # 默认启用
    
    base_module = False  # 是否为基础模块,如果是基础模块,被禁用后线程不会被删除
    is_active = False  # 模块是否正在运行
    
    def __init__(self):
        # 初始化模块属性
        self.name = self.__class__.name
        self.desc = self.__class__.desc
        self.tags = list(self.__class__.tags or [])
        self.topics = list(self.__class__.topics or [])
        self.triggers = list(self.__class__.triggers or [])
        
        self.base_module = self.__class__.base_module
        self.is_enable = self.__class__.is_enable
        
        self.ctx = None  # 存储传递给execute的上下文

    def execute(self, ctx):
        # 模块执行入口，子类需实现此方法
        self.ctx = ctx
        pass
    
    def _register(self):
        # 注册模块到全局注册表
        if self.__class__.__name__ == 'Base':
            return
        c._module_registry[self.name] = self
        c._trigger_registry[self.name] = self.triggers
        logging.getLogger("mgr").debug("registered %s, registry=%r", self.name, c._module_registry.keys())
                
            