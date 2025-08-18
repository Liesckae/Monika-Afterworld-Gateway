# -*- coding: utf-8 -*-
# 守护线程和守护线程管理器的实现
from __future__ import print_function, unicode_literals
import threading


__all__ = ['DaemonThread', 'DaemonManager']

lock = threading.Lock()

class DaemonThread(threading.Thread):
    # 守护线程类，用于执行模块任务
    def __init__(self, name, module, interval=10):
        import mgr.utils as utils
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
        # 线程运行逻辑，定期检查触发器并执行模块任务
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
        # 停止线程
        self.stopFlag.set()
    
    def __del__(self):
        # 线程销毁时记录日志
        self.logger.info('{} daemon thread quit.'.format(self.name))
    
class DaemonManager:
    # 守护线程管理器，用于管理多个守护线程
    def __init__(self, _module_registry, interval=10):
        import mgr.utils as utils
        
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
            
        utils.get_default_logger().debug('daemon threads started.')
    def run_all(self):
        # 启动所有模块的守护线程
        running_modules = []
        for name in self._module_registry.keys():
            if name not in self._threads.keys() and self.status.get(name):
                thread = DaemonThread(name, self._module_registry[name], self.interval)
                self._threads[name] = thread
                thread.start()
                running_modules.append(name)
        
            
    def stop_all(self):
        # 停止所有守护线程
        for t in self._threads.values():
            t.stop()
        for t in self._threads.values():
            t.join()
            
        self._threads.clear()
        
    def remove_module(self, module_name):
        # 移除指定模块的守护线程
        import mgr.utils as utils
        
        if not module_name in self._threads.keys():
            raise ValueError('%s module does not exists.' % module_name)
        self._threads[module_name].stop()
        self._threads[module_name].join()
        utils.set_module_status(module_name, False)
        
    def reload_all(self):
        # 重新加载所有模块状态并重启线程
        import mgr.utils as utils
        
        self.stop_all()
        utils.reload_module_status()
        self.run_all()
        
    def start(self):
        # 启动所有线程
        self.run_all()
        
    def reload_all_modules(self, module_registry, module_status):
        # 重新加载模块注册表和状态
        self._module_registry = module_registry
        self.status = module_status
        self.reload_all()
        
        