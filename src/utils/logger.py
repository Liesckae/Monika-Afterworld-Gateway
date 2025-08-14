import os
import logging
import src.utils.constants as constants

# Two integrierter loggers
# mag internal logger
m_logger = logging.getLogger('mag_logger')
# mas logger
logger = logging.getLogger('logger')

# Initialize
formatter = "%(asctime)s - %(levelname)s - %(name)s - %(message)s"
m_logger.setLevel(level=constants.M_LOGGER_LEVEL)
m_file_handler = logging.FileHandler(os.path.join(constants.LOG_PATH,constants.M_LOGGER_FILE))
m_file_handler.setFormatter(logging.Formatter(formatter))
m_logger.addHandler(m_file_handler)

class LoggerManager:

    def __init__(self):
        if not os.path.exists(constants.LOG_PATH):
            try:
                os.mkdir(constants.LOG_PATH)
            except Exception as e:
                m_logger.error("Can not create log path. {}".format(e))
                
        self._loggers = {}
        self.add_logger(m_logger)
        self.add_logger(logger)
        
    def add_logger(self, logger):
        """Add logger instance to logging registry

        Args:
            logger (logging.logger):  You know

        Returns:
            bool: True if operation is done without errors,and False otherwise.
        """
        if not isinstance(logger, logging.Logger):
            return False
        self._loggers.update({str(logger.name): logger})
        return True
        
    def remove_logger(self, logger_name):
        """Remove a logger from logging registry

        Args:
            logger_name (str): logger name to be removed.

        Returns:
            bool: True if operation is done without errors,and False otherwise.
        """
        if not isinstance(logger_name, str):
            return False
        del self._loggers[logger_name]
        return True
    
    def get_loggers(self):
        """Get all available loggers

        Returns:
            dict: All available loggers.
        """
        return self._loggers
    
    def get_logger(self, logger_name):
        """Get a logger.

        Args:
            logger_name (str): logger's name.

        Returns:
            loggging.logger: loggern object or None if logger not exist.
        """
        if not isinstance(logger_name, str):
            return None
        if not logger_name in self._loggers:
            return None
        return self._loggers[logger_name]
