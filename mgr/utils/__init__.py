# -*- coding: utf-8 -*-
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
    import mgr.logger as logger

    if not os.path.exists(path):
        try:
            os.makedirs(path)
        except OSError:
            raise Exception("Make dir error, path created by code is '{0}'.".format(path))
            
    logger.m_logger.info("Dir {0} check passed.".format(path))
    
def auto_check_path():
    for path in constants.PATH:
        check_path(path)

def get_default_logger():
    import mgr.logger as logger

    return logger.m_logger

def get_module_registry():
    return constants._module_registry

def get_trigger_registry():
    return constants._trigger_registry

def load_triggers():
    importlib.import_module(constants.triggers_path)

def load_module_status():
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
    return _module_status

def reload_module_status():
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
    global _module_status
    _module_status[name] = bool(enabled)
    save_module_status()