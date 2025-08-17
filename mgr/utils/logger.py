# -*- coding: utf-8 -*-
import logging
import constants

# mas日志，用于实现日志分离
logger = logging.getLogger("MAS")
# mgr内置日志器
m_logger = logging.getLogger("MGR")

logging.basicConfig(level=constants.m_logger_level,
                    format=constants.m_logger_format,
                    handlers=[logging.FileHandler(constants.m_log_file)]
                    )