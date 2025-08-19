# -*- coding: utf-8 -*-
# 调试触发器，用于测试和调试
from __future__ import print_function, unicode_literals
import base

class DebugTrigger(base.Base):
    # 调试触发器类，始终返回True
    def is_match(self):
        # 始终满足触发条件
        return True