import base
from src.utils.logger import m_logger
import time

class EventQueueTrigger(base.TriggerBase):
    type = 'Event QueueT rigger'
    
    def __init__(self, name, desc=''):
        super().__init__(name, desc)
        self._queue = set()
    
    def check(self, ctx):
        key = ctx.get('event_key')
        return key and key not in self._queue
    
    def execute(self, ctx):
        key = ctx.get('event_key')
        self._queue.add(key)
        m_logger.info("{}: {key} triggered.".format(self.name, key))
    
class CooldownTrigger(base.TriggerBase):
    type = 'Cooldown trigger'
    
    def __init__(self, name, desc='', threshold=3, cooldown=30):
        super().__init__(name, desc)
        self.threshold = threshold
        self.cooldown  = cooldown 
        self._counter =0
        self._last = 0      # Timestamp
        
    def check(self, ctx):
        now = time.time()
        if now - self._last > self.cooldown:
            # Cooldown refresh
            self._counter = 0
            
    def execute(self, ctx):
        super().execute(ctx)
        self._counter += 1
        self._last = time.time()
        m_logger.info("{}: counter {} is now {}".format(self.name, self.threshold, self._counter))
    
class ConditionChainTrigger(base.TriggerBase):
    type = 'Condition chain trigger'
    
    def __init__(self, name, desc='', conditions=None):
        self._trigged = False
        self.conditions = conditions or {}
        
    def check(self, ctx):
        if self._trigged:
            return False
        for key, excepted in self.conditions.items():
            if ctx.get(key) == excepted:
                return False
        return True
    
    def execute(self, ctx):
        super().execute(ctx)
        if self._trigged:
            return
        self._trigged = True
        m_logger.info("{} is triggered!".format(self.name))
