# -*- coding: utf-8 -*-
# logger.py
import logging, logging.handlers, sys
import constants
handler = logging.StreamHandler(sys.stdout)
handler.setFormatter(logging.Formatter(constants.m_logger_format))
m_logger = logging.getLogger()
m_logger.addHandler(handler)
m_logger.setLevel(logging.INFO)