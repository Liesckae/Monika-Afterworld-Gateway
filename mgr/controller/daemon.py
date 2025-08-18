# -*- coding: utf-8 -*-
from __future__ import print_function, unicode_literals
import threading
import mgr.utils as utils

__all__ = ['DaemonThread', 'DaemonManager']

lock = threading.Lock()

class DaemonThread(threading.Thread):
    def __init__(self, name, module, interval=10):
        threading.Thread.__init__(self)
        self.name = name
        self.interval = interval
        self.module = module
        self.daemon = True
        self.triggers = module.triggers
        self.logger = utils.get_default_logger()
        self.stopFlag = threading.Event()
        self.is_enable = module.is_enable
        self.is_running = False
        
    def run(self):
        while not getattr(self.stopFlag, 'is_set', self.stopFlag.isSet)():
            if not self.is_enable:
                self.stopFlag.wait(self.interval)
                continue

            try:
                args, kwargs = self.module.get_runtime_args() or ((), {})
                if all(t.is_match() for t in self.triggers):
                    self.module.execute(*args, **kwargs)
            except Exception as e:
                self.logger.exception("%s error: %s", self.name, e)
            self.stopFlag.wait(self.interval)
                                
        
    def stop(self):
        self.stopFlag.set()
    
    def __del__(self):
        self.logger.info('{} daemon thread quit.'.format(self.name))
    
class DaemonManager:
    def __init__(self, _module_registry, interval=10):
        self._module_registry = _module_registry
        self.interval = interval
        self._threads = {}
        self.status = utils.load_module_status()

        for name, module in _module_registry.items():
            if self.status.get(name):
                try:
                    thread = DaemonThread(name, module, self.interval)
                    thread.start()
                    self._threads[name] = thread
                except RuntimeError as e:
                    utils.get_default_logger().exception("start thread %s failed: %s", name, e)
            
    def run_all(self):
        running_modules = []
        for name in self._module_registry.keys():
            if name not in self._threads.keys() and self.status.get(name):
                thread = DaemonThread(name, self._module_registry[name], self.interval)
                self._threads[name] = thread
                thread.start()
                running_modules.append(name)
        
            
    def stop_all(self):
        
        for t in self._threads.values():
            t.stop()
        for t in self._threads.values():
            t.join()
            
        self._threads.clear()
        
    def remove_module(self, module_name):
        if not module_name in self._threads.keys():
            raise ValueError('%s module does not exists.' % module_name)
        self._threads[module_name].stop()
        self._threads[module_name].join()
        utils.set_module_status(module_name, False)
        
    def reload_all(self):
        self.stop_all()
        utils.reload_module_status()
        self.run_all()
        
    def start(self):
        self.run_all()
        
    def reload_all_modules(self, module_registry, module_status):
        self._module_registry = module_registry
        self.status = module_status
        self.reload_all()
        
        