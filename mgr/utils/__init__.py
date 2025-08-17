import os
import logger
import constants
import pkgutil
import importlib

def check_path(path):
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
    return logger.m_logger

def get_module_registry():
    return constants._module_registry

def get_trigger_registry():
    return constants._trigger_registry

def load_triggers():
    importlib.import_module(constants.triggers_path)

def load_modules():
    base_path = os.path.join(os.getcwd(), 'game', 'python-packages', 'mgr', 'modules')
    if not os.path.isdir(base_path):
        raise Exception("mgr/modules 目录不存在: {}".format(base_path))
        return

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
            raise Exception('load module fail: ' + modname)
def auto_load_modules():
    load_triggers()
    load_modules()