# -*- coding: utf-8 -*-
from __future__ import print_function, unicode_literals
import logging, os, pkgutil, importlib

import mgr.modules.test      # 这行会触发 Test 类
logging.getLogger("mgr").info("mgr/__init__.py forced import test")