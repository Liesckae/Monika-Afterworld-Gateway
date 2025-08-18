# -*- coding: utf-8 -*-
# 触发器基类，定义了触发器的基本结构和匹配逻辑
from __future__ import print_function, unicode_literals
import utils
m_logger = utils.get_default_logger()

class Base:
    # 触发器基类，所有触发器应继承此类
    def __init__(self, name=None, desc=None):
        # 初始化触发器属性
        self.name = name
        self.desc = desc
    def is_match(self):
        # 检查是否满足触发条件，子类需实现此方法
        pass
    