# -*- coding: utf-8 -*-
import os
import json
import threading
from datetime import datetime
from ..controller.daemon import DaemonManager
from .. import utils

class Core(object):
    _lock = threading.Lock()
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(Core, cls).__new__(cls)
        return cls._instance

    def __init__(self, log_prefix="mag", interval=30):
        if getattr(self, '_inited', False):
            return
        self._inited = True
        self.logger = utils.get_default_logger()
        self.dm = DaemonManager(utils.get_module_registry(), interval)

    def reload_all(self):
        with self._lock:
            self.dm.stop_all()
            utils.reload_module_status()
            self.dm.run_all()

    def start(self):
        self.dm.start()

    def stop(self):
        self.dm.stop_all()

    # 供 Ren'Py 直接调用
    def enable_module(self, name):
        utils.set_module_status(name, True)
        self.reload_all()

    def disable_module(self, name):
        utils.set_module_status(name, False)
        self.reload_all()

    def is_module_enabled(self, name):
        return utils.get_module_status().get(name, False)

# 单例暴露
def init(log_prefix="mag", interval=30):
    core = Core()
    return core.logger, core, core.dm