# -*- coding: utf-8 -*-
# 模块基类，定义了模块的基本结构和注册逻辑
from __future__ import print_function, unicode_literals
from datetime import datetime
import logging



class BaseMeta(type):
    # 元类，用于自动注册模块
    def __new__(cls, clsname, bases, clsdict):
        # Py2.7 写法：super 必须带参数
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
    
    def __init__(self):
        # 初始化模块属性
        self.name = self.__class__.name
        self.desc = self.__class__.desc
        self.tags = list(self.__class__.tags or [])
        self.topics = list(self.__class__.topics or [])
        self.triggers = list(self.__class__.triggers or [])
        self._args = None  # 存储传递给execute的参数
    
    def execute(self, *args, **kwargs):
        # 模块执行入口，子类需实现此方法
        pass
    
    def get_runtime_args(self):
        # 获取运行时参数
        return (datetime.now,), {}
    
    def _register(self):
        # 注册模块到全局注册表
        if self.__class__.__name__ == 'Base':
            return
        import mgr.utils.constants as c
        c._module_registry[self.name] = self
        c._trigger_registry[self.name] = self.triggers
        logging.getLogger("mgr").debug("registered %s, registry=%r",
                                       self.name, c._module_registry.keys())
                
            