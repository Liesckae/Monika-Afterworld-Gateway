import logging
import os

formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")

logging.basicConfig(level = logging.DEBUG,
                    format = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger('MAG_code')


file_handler = logging.FileHandler('log/mag_code.log')
file_handler.setFormatter(formatter)
file_handler.setLevel(logging.DEBUG)
logger.addHandler(file_handler)

if not os.path.exists(path='log'):
    with open('log/mag_code.log', 'w') as log_file:
        pass

logger.info('==========================================================================')
logger.info('Started MAG_Code\n\n')
    