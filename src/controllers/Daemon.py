# -*- coding: utf-8 -*-
import threading
import time
from src.utils.logger import m_logger

class Daemon_Thread(threading.Thread):
    def __init__(self, name, interval, module, run_fn, *args, **kargs):
        super().__init__()
        self.name = name
        self.interval = interval
        self.module = module
        self.run_fn = run_fn
        self.args = args
        self.kargs = kargs
        self.daemon = True
        
    def run(self):
        m_logger.debug("TreadL {} started, interval: {}, module: {}, run_fn: {}, args: {}, kargs: {}".format(self.name, self.interval, self.module, self.run_fn, self.args, self.kargs))
        while True:
            self.run_fn(*self.args, **self.kargs)
            time.sleep(self.interval)
    
    def __del__(self):
        m_logger.debug("Thread <{}> closed.".format(self.name))

class Daemon:
    def __init__(self, name, interval, module_registry={}, module_status={}):
        self.name = name
        self._module_registry = module_registry
        self._module_status = module_status
        self.interval = interval
        self._job_list = {}
        
        for module_name, cls in module_registry:
            # If cls has execute attribute, then add a thread into list
            if module_status[module_name] == True:
                run_fn = cls.execute
                thread = Daemon_Thread(cls.name, interval, cls, run_fn)
                self._job_list.update({module_name: thread})
            else:
                continue

        m_logger.debug("Job list : {}".format(self._job_list))
        
    def add_job(self, interval, cls):
        pass
    def delete_job(self, name):
        pass
    def reset_interval(self, interval):
        pass
    def reload_module(self, name):
        pass
    def reload_all_modules(self):
        pass