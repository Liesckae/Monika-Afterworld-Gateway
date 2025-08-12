from mag_scripts.actions.base import MetaBase
from mag_scripts.logger import logger

class Action(MetaBase):

    name = "TestAction"
    description = 'A testing action'

    def check(self, ctx):
        return ctx.get('name') == "TestAction" 

    def execute(self):
        logger.debug('Hello Monika!')


