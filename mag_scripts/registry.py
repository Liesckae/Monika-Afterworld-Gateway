import os
import importlib
import pathlib
from .actions.base import MetaBase
from mag_scripts.logger import logger

def load_modules():
    actions_dir = pathlib.Path(__file__).parent.absolute() / 'actions'
    logger.info(f"Action dir path is {actions_dir}")
    for py_file in actions_dir.glob("*.py"):
        if py_file.name == "__init__.py":
            continue
        name = py_file.stem
        importlib.import_module(f'.actions.{name}', __package__)
        logger.info(f"{name} is loaded")


def get_actions() -> dict[str, MetaBase]:
    return MetaBase._registry

def get_scripts() -> dict[str, list[str]]:
    return MetaBase._script_registry