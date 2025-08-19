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
        """
        守护线程主循环：
        • 一旦启动，除非外部 stop()，否则一直循环。
        • 每轮实时读取 self.module.is_enable：
            – False：仅 sleep，不退出线程（等外部把它改 True）。
            – True：检查 module.triggers 列表里所有触发器。
        • 仅当所有触发器的 is_match() 都返回 True 时才调用 execute()。
        • 当满足条件时，将每个触发器的execute()方法的返回值作为上下文传递给模块的execute()方法。
        • 任何异常只影响单轮，线程继续。
        """
        logger = self.logger
        stop_flag = self.stopFlag
        interval  = self.interval
        module    = self.module          # 局部变量加速访问

        while not (stop_flag.is_set() if hasattr(stop_flag, 'is_set') else stop_flag.isSet()):
            # 实时读取模块开关
            self.is_enable = module.is_enable
            if not self.is_enable:
                # 被禁用：空转等待
                stop_flag.wait(interval)
                continue

            try:
                # 要求所有触发器的 is_match() 都为 True
                triggers = module.triggers if module.triggers is not None else []
                if all(trigger.is_match() for trigger in triggers):
                    # 上下文
                    ctx = {trigger.name: trigger.execute({}) for trigger in triggers}
                    module.execute(ctx)

            except Exception as e:
                logger.exception("%s error: %s", self.name, e)

            # 等下一轮
            stop_flag.wait(interval)

        logger.info('%s daemon thread quit.', self.name)
                                
        
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
        # 只关闭已启动的线程
        for t in list(self._threads.values()):
            if t.is_alive():
                t.stop()
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
        
        