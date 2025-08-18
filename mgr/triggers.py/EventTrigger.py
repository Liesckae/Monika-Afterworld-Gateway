# -*- coding: utf-8 -*-
# 事件触发器，包括队列触发、冷却触发和条件链触发
from __future__ import print_function, unicode_literals
import base
import time
import utils

m_logger = utils.get_default_logger()


class EventQueueTrigger(base.Base):
    """触发一次后把 key 加入队列，避免重复触发"""
    type = 'EventQueueTrigger'

    def __init__(self, name, desc=''):
        # 初始化事件队列触发器
        super(base.Base, self).__init__(name, desc)
        self._seen = set()          # 已触发过的 key

    def is_match(self, ctx=None):
        # 检查是否满足触发条件
        key = ctx and ctx.get('event_key')
        if key and key not in self._seen:
            self._seen.add(key)
            return True
        return False


class CooldownTrigger(base.Base):
    """连续触发 N 次后进入冷却"""
    type = 'CooldownTrigger'

    def __init__(self, name, desc='', threshold=3, cooldown=30):
        # 初始化冷却触发器
        super(base.Base, self).__init__(name, desc)
        self.threshold = threshold
        self.cooldown = cooldown
        self._count = 0
        self._last = 0

    def is_match(self, ctx=None):
        # 检查是否满足触发条件
        now = time.time()
        if now - self._last > self.cooldown:
            self._count = 0

        if now - self._last > self.cooldown:
            self._count = 0
            self._last = now
        self._count += 1
        return self._count >= self.threshold


class ConditionChainTrigger(base.Base):
    """当所有条件键均匹配时触发一次"""
    type = 'ConditionChainTrigger'

    def __init__(self, name, desc='', conditions=None):
        # 初始化条件链触发器
        super(base.Base, self).__init__(name, desc)
        self.conditions = conditions or {}   # {key: expected_value}

    def is_match(self, ctx=None):
        # 检查是否满足所有条件
        if not ctx:
            return False
        return all(ctx.get(k) == v for k, v in self.conditions.items())