import utils

class ModuleManager:
    def __init__(self):
        # 应该保持整个子模组运行过程中只有一个ModuleManager实例
        self._register = utils.get_module_registry()
        self.module_status = utils.get_module_status()
    def add_module(self, module_class):
        # 手动添加一个模块，用于调试
        self._register[module_class.name] = module_class
    def get_modules(self):
        return self._register
    def set_module_status(self, name, status):
        if not name in utils.load_module_status().keys():
            raise Exception('Module: {} not exists.'.format(name))
        utils.load_module_status()[name] = status
    def enable(self, module_name):
        self.set_module_status(module_name, True)
    def disable(self, module_name):
        self.set_module_status(module_name, False)
        

class TriggerManager:
    def __init__(self):
        self._register = utils.get_trigger_registry()
    def add_trigger(self, module_name, trigger):
        # 这个和下面那个都是调试用的，看需求用,反正utils里面没有这个接口，要用自己import
        self._register[module_name].append(trigger)
    def del_trigger(self, module_name, trigger):
        self._register[module_name].remove(trigger)
    
    