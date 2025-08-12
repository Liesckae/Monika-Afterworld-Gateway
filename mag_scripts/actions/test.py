from mag_scripts.actions.base import MetaBase
from mag_scripts.logger import logger
import mag_scripts.actions.base as base

class Action(MetaBase):

    name = "test"
    description = ''
    topic = "test_topic"
    triggers = [base.DebugTrigger]

    @classmethod
    def set_topic(cls, topic):
        cls.topic = topic

    def __init__(self):
        super(Action, self).__init__() 

    @classmethod
    def execute(cls):
        logger.info(u'Test module executed')


