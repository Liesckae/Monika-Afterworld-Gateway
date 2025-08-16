# -*- coding: utf-8 -*-
import src.utils.constants
import src.actions.base
import src.utils.file_ops as file_ops
import src.utils.logger as logger

l_manager = logger.LoggerManager()
m_logger = l_manager.get_logger('m_logger')

def get_module_registry():
    return src.actions.base.ActionBase._module_registry

def get_module_status():
    return file_ops.read_module_status()


    