# -*- coding: utf-8 -*-
import os,sys
from src.utils.logger import m_logger
import src.utils.constants as constants
from src.actions.base import ActionManager
from src.triggers.base import TriggerManager
from src.controllers.Daemon import Daemon
def init(daemon_name, interval):
    """
    Initialization steps
    1. Init logger
    2. Check and create necessary dirs
    3. Load triggers
    4. Load modules
    5. Init Daemon
    """
    # init logger
    m_logger.info("Initializing core module...")

    # Check dirs
    required_dirs = constants.PATH
    for dir_name in required_dirs:
        check_path(dir_name)
        m_logger.debug(f"Directory {dir_name} is ready.")
        
    #load trigger manager
    triggermanager = TriggerManager()
    
    # load module manager
    module_manager = ActionManager()
    
    # Init Daemon
    daemon = Daemon(name=daemon_name, interval=interval, module_registry=module_manager.get_module_registry(), module_status=module_manager.get_status())

def check_path(path):
    if os.path.exists(path):
        try:
            os.system("mkdir {}".format(path))
        except Exception as e:
            m_logger.error("Can not create path. {}".format(e))

def load_module():
    pass