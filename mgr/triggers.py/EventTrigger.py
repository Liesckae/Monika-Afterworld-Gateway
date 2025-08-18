# -*- coding: utf-8 -*-
from __future__ import print_function, unicode_literals
import base
import time
import utils

m_logger = utils.get_default_logger()


class EventQueueTrigger(base.Base):
    """触发一次后把 key 加入队列，避免重复触发"""
    type = 'EventQueueTrigger'

    def __init__(self, name, desc=''):
        super(base.Base, self).__init__(name, desc)
        self._seen = set()          # 已触发过的 key

    def is_match(self, ctx=None):
        key = ctx and ctx.get('event_key')
        if key and key not in self._seen:
            self._seen.add(key)
            return True
        return False


class CooldownTrigger(base.Base):
    """连续触发 N 次后进入冷却"""
    type = 'CooldownTrigger'

    def __init__(self, name, desc='', threshold=3, cooldown=30):
        super(base.Base, self).__init__(name, desc)
        self.threshold = threshold
        self.cooldown = cooldown
        self._count = 0
        self._last = 0

    def is_match(self, ctx=None):
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
        super(base.Base, self).__init__(name, desc)
        self.conditions = conditions or {}   # {key: expected_value}

    def is_match(self, ctx=None):
        if not ctx:
            return False
        return all(ctx.get(k) == v for k, v in self.conditions.items())