from abc import abstractmethod

class MetaBase:
    # Registry of actions and their name and description.
    _registry = {}

    # Registration behavior
    def __init_subclass__(cls,**kw):
        super().__init_subclass__(**kw)
        name = getattr(cls,'name', None)
        # Checker
        if not name or not isinstance(name, str) or len(name) < 1:  
            raise TypeError(
                f'{cls.__name__} Must define a non-empty string class attribute "name"'
                )
        if name in MetaBase._registry:
            raise TypeError(f'"name"{name} already exists')     
        
    @abstractmethod
    def check(self,ctx: dict) -> bool:
       ...

    @abstractmethod
    def execute(self,ctx: dict):
        ...
    # TODO: 完成Monika演出的字典形式
    def script(self, ctx: dict) -> list[dict]:
        return []
        
    
        