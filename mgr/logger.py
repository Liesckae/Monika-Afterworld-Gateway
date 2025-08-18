# -*- coding: utf-8 -*-
# logger.py
import logging, logging.handlers, sys
import mgr.utils.constants as constants
import os
handler = logging.FileHandler(constants.m_log_file)
handler.setFormatter(logging.Formatter("%(asctime)s:%(levelname)s:%(name)s:%(message)s"))
m_logger = logging.getLogger("mgr")
m_logger.addHandler(handler)
m_logger.setLevel(logging.DEBUG)