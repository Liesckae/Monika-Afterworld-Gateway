from mag_scripts.actions.base import MetaBase
from mag_scripts.logger import logger
import mag_scripts.actions.base as base
import subprocess,sys,os

class Action(MetaBase):

    name = "mag_test"
    description = 'test'
    topic = "test_topic"
    triggers = [base.DebugTrigger]

    def __init__(self):
        super(Action, self).__init__()

    @classmethod
    def set_topic(cls, topic):
        cls.topic = topic

    @classmethod
    def execute(cls):
        
        current_dir = os.path.dirname(os.path.abspath(__file__))
        gateway_root = os.path.abspath(os.path.join(current_dir, '..', '..'))
        code_dir = os.path.join(gateway_root, 'mag_code')
        code_path = os.path.join(code_dir, 'mag_test.py')

        if not os.path.isdir(code_dir):
            logger.error("mag_code directory not found: %s" % code_dir)
            return
        if not os.path.isfile(code_path):
            logger.error("mag_test.py not found: %s" % code_path)
            return

        cls.run(code_path)

            



