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
        logger.debug(u'current path %s' %os.getcwd())
        try:
            logger.debug(u'%s execute path: %s' % (cls.name, cls.get_code_path()))
            code_path = cls.get_code_path()+'/'+cls.name+'.py'
            if os.path.exists(code_path):
                logger.debug('code path exists')
            else:
                logger.error('code path not exists')
                raise Exception("The code for action %s not exists"%cls.name)
            logger.info(u'%s action executed' % cls.name)
            subprocess.Popen([sys.executable, cls.get_code_path()+"/test.py"])
            
            
            cls.enable_module(cls.name)
        except Exception as e:
            logger.error(u"execute error: %s" % str(e))

            raise
        finally:
            logger.info(u"execute complete")


