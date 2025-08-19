# 这个模块用于模拟记录莫妮卡的行为，可能被一些模块依赖
# 这个模块将模拟入侵MAS的日志文件mas_log.log
# 与其他模块不同的是,禁用这个模块仅仅只是禁用了写入功能,不会删除线程

from mgr.modules.base import Base
from mgr.triggers.BaseModuleTriggers import LogInvasionTrigger
import logging
import mgr.utils.constants as c
import renpy
import os

log_file = os.path.join(renpy.config.gamedir,'..', 'log', c.cfg.get('log_invasion', 'target_file')) 

class LogInvasion(Base):
    name = 'log_invasion'
    desc = '日志入侵模块,用于模拟入侵MAS日志文件,给一些模块提供附加功能'
    tags = None
    topics = None
    triggers = [LogInvasionTrigger()]     # 触发器列表，当所有触发器的check方法都返回true时，将执行模块的执行入口，名字不是必填的，
                        # 但是为了能找到触发器，建议填写
    is_enable = True        # 默认启用
    
    base_module = True  # 是否为基础模块,如果是基础模块,被禁用后线程不会被删除
    is_active = False  # 模块是否正在运行,暂未使用
    
    def __init__(self):
        # 初始化模块属性
        self.name = self.__class__.name
        self.desc = self.__class__.desc
        self.tags = list(self.__class__.tags or [])
        self.topics = list(self.__class__.topics or [])
        self.triggers = list(self.__class__.triggers or [])
        
        self.base_module = self.__class__.base_module
        self.is_enable = self.__class__.is_enable
        
        self.ctx = None  # 存储传递给execute的上下文
        
        self.loggers = {}
        self.logger = logging.getLogger("unknown")
        
        file_handler = logging.FileHandler(log_file, encoding='UTF-8')
        self.logger.setLevel(logging.DEBUG)
        file_handler.setFormatter(logging.Formatter("%(asctime)s:%(name)s:%(message)s"))
        self.logger.addHandler(file_handler)
        
        self.loggers['basic'] = self.logger
        
    def execute(self, ctx):
        pass

    def invade_log(self, name="basic", msg=None):
            # 你都用这个接口了，肯定是不会用到调试的对吧
            if self.is_enable:
                if name not in self.loggers:
                    raise KeyError("logger {} not found".format(name))
                self.loggers[name].info(msg)
            else:
                pass
    def register_logger(self, name):
        if name not in self.loggers:
            self.loggers[name] = logging.getLogger(name)
            file_handler = logging.FileHandler(log_file, encoding='UTF-8')
            self.loggers[name].addHandler(file_handler)
            self.loggers[name].setLevel(logging.DEBUG)
            self.loggers[name].handlers[0].setFormatter(logging.Formatter("%(asctime)s:%(name)s:%(message)s"))
    def unregister_logger(self, name):
        if name in self.loggers:
            del self.loggers[name]
        else:
            raise KeyError("logger {} not found".format(name))
        
    def get_logger(self, name):
        if name in self.loggers:
            return self.loggers[name]
        else:
            raise KeyError("logger {} not found".format(name))  