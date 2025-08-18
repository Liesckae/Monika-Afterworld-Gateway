# -*- coding: utf-8 -*-
# 工具包的初始化文件，包含模块状态管理、路径检查和线程管理等功能
from __future__ import print_function, unicode_literals
import os
import constants
import pkgutil
import importlib
import json
import threading

import mgr.controller.daemon


_STATUS_FILE = os.path.join(constants.util_path, 'module_status.json')
_module_status = {}

_THREADS = {}
_LOCK = threading.Lock()
_SAVE_LOCK = threading.Lock()

def check_path(path):
    # 检查路径是否存在，不存在则创建
    import mgr.logger as logger

    if not os.path.exists(path):
        try:
            os.makedirs(path)
        except OSError:
            raise Exception("Make dir error, path created by code is '{0}'.".format(path))
            
    logger.m_logger.info("Dir {0} check passed.".format(path))
    
def auto_check_path():
    # 自动检查所有路径
    for path in constants.PATH:
        check_path(path)

def get_default_logger():
    # 获取默认日志记录器
    import mgr.logger as logger

    return logger.m_logger

def get_module_registry():
    # 获取模块注册表
    return constants._module_registry

def get_trigger_registry():
    # 获取触发器注册表
    return constants._trigger_registry

def load_triggers():
    # 加载所有触发器
    importlib.import_module(constants.triggers_path)

def load_module_status():
    # 加载模块状态
    global _module_status
    if not os.path.isfile(_STATUS_FILE) or os.path.getsize(_STATUS_FILE) == 0:
        _module_status = {name: mod.is_enable
                          for name, mod in get_module_registry().items()}
        # 目录不存在则自动创建
        try:
            os.makedirs(os.path.dirname(_STATUS_FILE))
        except OSError as e:
            if e.errno != errno.EEXIST:
                raise
        _module_status = {name: mod.is_enable for name, mod in get_module_registry().items()}
        with open(_STATUS_FILE, 'w') as f:
            json.dump(_module_status, f, indent=2)
    else:
        with open(_STATUS_FILE, 'r') as f:
            _module_status = json.load(f)
    return _module_status

def save_module_status():
    # 保存模块状态
    with _SAVE_LOCK:
        tmp = _STATUS_FILE + '.tmp'
        try:
            with open(tmp, 'w') as f:
                json.dump(_module_status, f, indent=2)
            if os.path.exists(_STATUS_FILE):
                os.remove(_STATUS_FILE)
            os.rename(tmp, _STATUS_FILE)
        except (IOError, OSError) as e:
            if os.path.exists(tmp):
                os.remove(tmp)
            raise

def get_module_status():
    # 获取模块状态
    return _module_status

def reload_module_status():
    # 重新加载模块状态
    global _module_status
    registry = get_module_registry()
    status_keys = set(_module_status)
    registry_keys = set(registry)
    
    for key in registry_keys - status_keys:
        _module_status[key] = registry[key].is_enable

    for key in status_keys - registry_keys:
        _module_status.pop(key, None)
        
    if (status_keys ^ registry_keys):
        save_module_status()

def load_modules():
    # 加载所有模块
    base_path = os.path.join(os.getcwd(), 'game', 'python-packages', 'mgr', 'modules')
    if not os.path.isdir(base_path):
        raise Exception("mgr/modules 目录不存在: {}".format(base_path))

    # 把目录拼成包名
    pkg_name = 'mgr.modules'

    try:
        root = importlib.import_module(pkg_name)
    except ImportError:
        raise Exception("Load module <{}> import error".format(pkg_name))

    for _, modname, _ in pkgutil.walk_packages(root.__path__, root.__name__ + '.'):
        try:
            importlib.import_module(modname)
            
        except Exception as e:
            get_default_logger().exception('load module %s failed: %s', modname, e)
        
def auto_load_modules():
    # 自动加载所有模块
    load_triggers()
    load_modules()
    reload_module_status()
    
def start_thread(name, module, interval=10):
    """手动启动单个模块线程"""
    with _LOCK:
        if name in _THREADS and _THREADS[name].is_alive():
            get_default_logger().warning('%s already running', name)
            return
        t = mgr.controller.daemon.DaemonThread(module.name, module, interval)
        t.start()
        _THREADS[name] = t
        get_default_logger().info('%s thread started', name)
        
def stop_thread(name, timeout=5):
    """安全停止单个 DaemonThread"""
    with _LOCK:
        t = _THREADS.pop(name, None)
        if t and t.is_alive():
            t.stop()
            t.join(timeout)
            get_default_logger().info('%s DaemonThread stopped', name)
        else:
            get_default_logger().warning('%s not running', name)
            
def set_module_status(name, enabled):
    # 设置模块状态
    global _module_status
    _module_status[name] = bool(enabled)
    save_module_status()