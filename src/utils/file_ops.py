# -*- coding: utf-8 -*-
import src.utils.constants as constants
import json
import os

def read_module_status():
    """Read module status

    Returns:
        dict: {str, bool}: module status
    """
    if not os.path.exists(constants.MODULE_STATUS_FILE):
        return None
    with open(constants.MODULE_STATUS_FILE, 'r', encoding='UTF-8') as f:
        module_status = json.loads(f.read())
    return module_status

def save_module_status(module_status):
    """Save module_status

    Args:
        module_status (dict: {str, bool}): module status.

    Returns:
        bool: True if write is completed and False otherwise.
    """
    if not os.path.exists(constants.DATA_PATH):
        return False
    with open(constants.MODULE_STATUS_FILE, 'w', encoding='UTF-8') as f:
        f.write(json.dumps(module_status))
        return True

def load_module_status():
    pass
