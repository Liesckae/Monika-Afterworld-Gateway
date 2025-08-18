# -*- coding: utf-8 -*-
# logger.py
import logging, logging.handlers, sys
import constants
import os
handler = logging.FileHandler(constants.m_log_file)
handler.setFormatter(logging.Formatter(constants.m_logger_format))
m_logger = logging.getLogger("mgr")
m_logger.addHandler(handler)
m_logger.setLevel(logging.INFO)