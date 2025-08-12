import os
import imp
import inspect
from mag_scripts.actions.base import MetaBase
from mag_scripts.logger import logger

def load_modules():
    n = 0
    # Get the directory path of the current file
    current_path = os.path.abspath(inspect.getfile(inspect.currentframe()))
    current_dir = os.path.dirname(current_path)
    actions_dir = os.path.join(current_dir, 'actions')
    logger.info("Action dir path is %s" % actions_dir)
    
    # Iterate through all .py files in the actions directory
    for filename in os.listdir(actions_dir):
        if filename.endswith('.py') and filename != '__init__.py':
            # Extract module name
            module_name = filename[:-3]
            # Import the module
            module_path = os.path.join(actions_dir, filename)
            imp.load_source('.actions.%s' % module_name, module_path)
            logger.info("%s is loaded" % module_name)
            n += 1
    
    logger.info('%d modules were loaded' % n)
    logger.debug('%s' % MetaBase._registry)
    logger.debug('%s' % MetaBase._topic_registry)


def get_actions():
    return MetaBase._registry

def get_topics():
    return MetaBase._topic_registry