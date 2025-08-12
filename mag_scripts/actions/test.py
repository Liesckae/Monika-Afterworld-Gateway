from mag_scripts.actions.base import MetaBase
from mag_scripts.logger import logger

class Action(MetaBase):

    name = "TestAction"
    description = 'A testing action'

    def check(self, ctx: dict) -> bool:
        return ctx.get('name') == "TestAction" 
    def execute(self):
        print("Hello Monika!")
        logger.debug('Hello Monika!')


