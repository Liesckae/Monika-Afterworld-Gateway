# 这个模块用于定义一些基础模块特有的触发器

import mgr.triggers.base as base

class LogInvasionTrigger(base.Base):
    name = 'log_invasion'
    desc = ''
    times = 0
    
    def __init__(self):
        pass

    def is_match(self):
        # 测试状态，持续返回真
        if self.times > 0:
            return False
        else:
            self.times += 1
            return True