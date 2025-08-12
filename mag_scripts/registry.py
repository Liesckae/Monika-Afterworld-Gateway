import os
import importlib
import pathlib
from mag_scripts.actions.base import MetaBase
from mag_scripts.logger import logger

def load_modules():
    n = 0
    actions_dir = pathlib.Path(__file__).parent.absolute() / 'actions'
    logger.info(u"Action dir path is %s" % actions_dir)
    for py_file in actions_dir.glob("*.py"):
        if py_file.name == "__init__.py":
            continue
        name = py_file.stem
        importlib.import_module(u'.actions.%s' % name, __package__)
        logger.info(u"%s is loaded" % name)
        n += 1
    logger.info(u'%d modules were loaded' % n)
    logger.debug(u'%s' % MetaBase._registry)
    logger.debug(u'%s' % MetaBase._topic_registry)


def get_actions():
    return MetaBase._registry

def get_topics():
    return MetaBase._topic_registry