# -*- coding: utf-8 -*-
from __future__ import print_function, unicode_literals
from datetime import datetime
import logging



class BaseMeta(type):
    def __new__(cls, clsname, bases, clsdict):
        # Py2.7 写法：super 必须带参数
        new_cls = super(BaseMeta, cls).__new__(cls, clsname, bases, clsdict)
        if clsname != 'Base':
            inst = new_cls()
            inst._register()
        return new_cls
        

class Base(object):
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
    
    def execute(self, *args, **kwargs):
        # 这是每个模块的执行入口，调用之前先把参数传递进来
        pass
    
    def get_runtime_args(self):
        return (datetime.now,), {}
    
    def _register(self):
        if self.__class__.__name__ == 'Base':
            return
        import mgr.utils.constants as c
        c._module_registry[self.name] = self
        c._trigger_registry[self.name] = list(self.triggers)
        logging.getLogger("mgr").debug("registered %s, registry=%r",
                                       self.name, c._module_registry.keys())
                
            