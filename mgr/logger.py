# -*- coding: utf-8 -*-
# logger.py
# 日志模块，用于配置和管理日志记录
import logging
import mgr.utils.constants as constants


# 设置日志文件路径和格式
handler = logging.FileHandler(constants.m_log_file)
handler.setFormatter(logging.Formatter("%(asctime)s:%(levelname)s:%(name)s:%(message)s"))
handler.encoding = 'UTF-8'

# 创建日志记录器并配置
m_logger = logging.getLogger("mgr")
m_logger.addHandler(handler)
m_logger.setLevel(logging.DEBUG)
