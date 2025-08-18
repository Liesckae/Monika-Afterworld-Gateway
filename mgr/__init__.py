# -*- coding: utf-8 -*-
# 模块初始化文件
from __future__ import print_function, unicode_literals
import logging, os, pkgutil, importlib

# 强制导入测试模块并记录日志
import mgr.modules.test      # 这行会触发 Test 类
logging.getLogger("mgr").info("mgr/__init__.py forced import test")