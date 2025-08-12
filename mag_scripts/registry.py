import os
import importlib
import pathlib
from mag_scripts.actions.base import MetaBase
from mag_scripts.logger import logger

def load_modules():
    n = 0
    actions_dir = pathlib.Path(__file__).parent.absolute() / 'actions'
    logger.info(f"Action dir path is {actions_dir}")
    for py_file in actions_dir.glob("*.py"):
        if py_file.name == "__init__.py":
            continue
        name = py_file.stem
        importlib.import_module(f'.actions.{name}', __package__)
        logger.info(f"{name} is loaded")
        n += 1
    logger.info(f'{n} modules were loaded')
    logger.debug(f'{MetaBase._registry}')
    logger.debug(f'{MetaBase._topic_registry}')



def get_actions() -> dict[str, MetaBase]:
    return MetaBase._registry

def get_topics() -> dict[str, list[str]]:
    return MetaBase._topic_registry