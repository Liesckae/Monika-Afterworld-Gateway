import os
import configparser

# This variable is used in test environment
# ROOT_PATH = os.path.join(os.getcwd(), '..')
ROOT_PATH = os.path.join(os.getcwd(), 'game', 'Submods', 'Monika-Afterworld-Gateway')
CONFIG_FILE = os.path.join(ROOT_PATH, 'config.ini')
cfg = configparser.ConfigParser()
cfg.read(CONFIG_FILE)

DATA_PATH = cfg.get('paths', 'data_dir')
SCRIPTS_PATH = cfg.get('paths', 'scripts_dir')
LOG_PATH = cfg.get('paths', 'log_dir')
SRC_PATH = cfg.get('paths', 'src_dir')
TOOLS_PATH = cfg.get('paths', 'tools_dir')
TRIGGERS_PATH = cfg.get('paths', 'triggers_dir')


LOGGERS_REGISTRY = {}
LOGGER_LEVEL = cfg.get('logger', 'logging_level')
M_LOGGER_LEVEL = cfg.get('logger', 'mag_logging_level')
M_LOGGER_FILE = cfg.get('logger', 'mag_logging_file')

MODULE_REGISTRY = {}
MODULE_STATUS = {}
MODULE_STATUS_FILE = os.path.join(ROOT_PATH, DATA_PATH, cfg.get('config', 'module_status_file'))

TRIGGERS_REGISTRY = {}
