# -*- coding: utf-8 -*-
import os
import ConfigParser
# 因为renpy太老旧了没有接口（反正我没找到，如果你有建议的话直接PR就好了），所以我只有直接用python来定义
# 子模组运行路径是在游戏根目录的，所以需要拼接目录
game_path = os.getcwd()
root_path = os.path.join(game_path, 'game', 'Submods', 'Monika-Afterworld-Gateway')
python_package_path = os.path.join(game_path, 'game', 'python-packages', 'mgr')

# =================================================
# 存放路径
# 子模组内部文件路径
# Submods目录下
data_path = os.path.join(root_path, 'data')
log_path = os.path.join(root_path, 'logs')
# python包目录下
mgr_path = os.path.join(python_package_path, 'mgr')
controller_path = os.path.join(mgr_path, 'controller')
core_path = os.path.join(mgr_path, 'core')
modules_path = os.path.join(python_package_path, 'modules')
triggers_path = os.path.join(mgr_path, 'triggers')
util_path = os.path.join(mgr_path, 'utils')
PATH = [data_path, log_path, mgr_path, controller_path, core_path, modules_path, triggers_path, util_path]
# ==================================================

# ==================================================
# 一些注册表
_module_registry = {}      # 模块注册表
_trigger_registry = {}      # 触发器注册表
_daemin_registry = {}       # 守护进程注册表
# =================================================

# =================================================
# 一些可配置项
config_file = os.path.join(root_path, 'config.ini')   # 配置文件路径

cfg = ConfigParser.ConfigParser()
cfg.read(config_file)


m_log_file = os.path.join(cfg.get('logger', 'm_log_file'))
m_logger_level = cfg.get('logger', 'm_logger_level')
m_logger_format = cfg.get('logger', 'm_logger_format')
# ================================================
