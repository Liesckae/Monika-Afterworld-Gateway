# -*- coding: utf-8 -*-
# 随机触发器，基于概率触发
from __future__ import print_function, unicode_literals
import mgr.modules.base as base
import random

class RandomTrigger(base.Base):
    type = 'Random Trigger'
    
    def __init__(self, name='', desc='', probability=0):
        """Initialize when the subclass is instantiates

        Args:
            name (str): The name of the instance
            desc (str, optional): Description of this instance. Defaults to ''.
            probability (int, optional): The probability (0 - 1.0) that the trigger should execute.Defaults to 0.
        """
        # 初始化随机触发器
        self.probability = probability
        
    def is_match(self):
        """Check if should execute

        Returns:
            bool: True if meet the condition; False if not
        """
        # 基于概率检查是否满足触发条件
        return random.random() < self.probability

    