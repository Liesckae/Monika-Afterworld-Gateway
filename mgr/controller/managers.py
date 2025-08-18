# -*- coding: utf-8 -*-
# 模块管理器和触发器管理器的实现
from __future__ import print_function, unicode_literals
import utils

class ModuleManager:
    # 模块管理器，用于管理模块的注册和状态
    def __init__(self):
        # 应该保持整个子模组运行过程中只有一个ModuleManager实例
        self._register = utils.get_module_registry()
        self.module_status = utils.get_module_status()
    def add_module(self, module_class):
        # 手动添加一个模块，用于调试
        self._register[module_class.name] = module_class
    def get_modules(self):
        # 获取所有模块
        return self._register
    def set_module_status(self, name, status):
        # 设置模块状态
        if not name in utils.load_module_status().keys():
            raise Exception('Module: {} not exists.'.format(name))
        utils.load_module_status()[name] = status
    def enable(self, module_name):
        # 启用模块
        self.set_module_status(module_name, True)
    def disable(self, module_name):
        # 禁用模块
        self.set_module_status(module_name, False)
        

class TriggerManager:
    # 触发器管理器，用于管理触发器的注册和移除
    def __init__(self):
        self._register = utils.get_trigger_registry()
    def add_trigger(self, module_name, trigger):
        # 这个和下面那个都是调试用的，看需求用,反正utils里面没有这个接口，要用自己import
        self._register[module_name].append(trigger)
    def del_trigger(self, module_name, trigger):
        # 移除触发器
        self._register[module_name].remove(trigger)
    
    