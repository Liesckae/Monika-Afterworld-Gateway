# -*- coding: utf-8 -*-
# 核心模块，提供单例模式的核心功能
from __future__ import print_function, unicode_literals
import os
import json
import threading
from datetime import datetime
from ..controller.daemon import DaemonManager
from .. import utils

import logging

class Core(object):
    # 核心类，管理模块和线程
    _lock = threading.Lock()
    _instance = None

    def __new__(cls):
        utils.get_default_logger().debug("init mgr.core.")

        
        if cls._instance is None:
            cls._instance = super(Core, cls).__new__(cls)
        return cls._instance

    def __init__(self, log_prefix="mag", interval=30):
        # 初始化核心模块
        if getattr(self, '_inited', False):
            return
        self._inited = True
        self.logger = utils.get_default_logger()
        self.dm = DaemonManager(utils.get_module_registry(), interval)
        
        utils.get_default_logger().info("Core created DaemonManager with %d modules", len(self.dm._threads))
        self.logger.info("registry keys before DaemonManager: %s", list(utils.get_module_registry().keys()))

    def reload_all(self):
        # 重新加载所有模块状态
        with self._lock:
            self.dm.stop_all()
            utils.reload_module_status()
            self.dm.run_all()

    def start(self):
        # 启动所有线程
        self.dm.start()

    def stop(self):
        # 停止所有线程
        self.dm.stop_all()

    # 供 Ren'Py 直接调用
    def enable_module(self, name):
        # 启用指定模块
        utils.set_module_status(name, True)
        self.reload_all()

    def disable_module(self, name):
        # 禁用指定模块
        utils.set_module_status(name, False)
        self.reload_all()

    def is_module_enabled(self, name):
        # 检查模块是否启用
        return utils.get_module_status().get(name, False)

    def refresh_module_registry(self):
        # 刷新模块注册表
        utils.reload_module_status()
        self.dm.reload_all_modules(utils.get_module_registry(), utils.get_module_status())

    def set_status(self, name, status):
        # 设置模块状态
        utils.set_module_status(name, status)

    def get_module_registry(self):
        # 获取模块注册表
        return utils.get_module_registry()

    def get_status(self):
        # 获取模块状态
        return utils.get_module_status()

# 单例暴露
def init(log_prefix="mag", interval=30):
    # 初始化核心模块并返回实例
    utils.get_default_logger().debug("init module mgr.")

    
    core = Core()
    return core.logger, core, core.dm