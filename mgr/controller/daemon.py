import threading
from time import sleep
import utils

lock = threading.Lock()

class DaemonThread(threading.Thread):
    def __init__(self, name, module, interval=10, *args, **kw):
        threading.Thread.__init__(self)
        self.stopFlag = False
        self.name = name
        self.interval = interval
        self.module = module
        self.args = args
        self.kw = kw
        self.daemon = True
        self.stopFlag = False
        self.triggers = module.triggers
        self.logger = utils.get_default_logger()
        self.is_enable = module.is_enable
        
    def run(self):
        list = []
        if self.is_enable:
            while not self.stopFlag:
                lock.acquire()
                
                for trigger in self.triggers:
                    list.append(trigger.is_match)
                
                if all(list):
                    self.module.execute(self.module.args)
                
                sleep(self.interval)
                lock.release()
        
    def stop(self):
        self.stopFlag = True
    
    def __del__(self):
        pass
    
class DaemonManager:
    def __init__(self, _module_registry, intervel=10):
        self.intervel = intervel
        self._treads = {}
        for name, module in _module_registry.items():
            DaemonThread(name, module, self.intervel).start()
            self._treads[name] = module
            
    def start_all(self):
        for name, t in self._treads.items():
            t.start()
    def stop_all(self):
        for name, t in self._treads.items():
            t.stop()
    def disable(self, name):
        if name in self._treads.keys():
            self._treads[name].stop()
            self._treads.is_enable = False
    def add_daemon(self):
        pass
    def del_daemon(self, daemon_name):
        pass
    def __del__(self):
        pass
    