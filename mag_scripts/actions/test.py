from base import MetaBase

class Action(MetaBase):

    name = "TestAction"
    description = 'A testing action'

    def check(self, ctx: dict) -> bool:
        return ctx.get('name') == "TestAction" 
    def run(self,ctx: dict):
        print("Hello Monika!")
    def script(self, ctx: dict) -> list[dict]:
        return super().script(ctx)
    
# Test code
if __name__ == '__main__':

    ctx = {}

    Action().run(ctx)
