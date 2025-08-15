import base

class DebugTrigger(base.TriggerBase):
    # This trigger is for testing purposes.
    
    type = 'Debug trigger'
    
    def __init__(self, name, desc=''):
        """Initialize when the subclass is instantiated

        Args:
            name (str): The name of the instance
            desc (str, optional): Description of this instance. Defaults to ''.
        """
        super().__init__(name, desc)
        
    def check(self, ctx):
        """Check if should execute

        Args:
            ctx (any): Reserved parameters

        Returns:
            bool: Always returns True for debug purposes
        """
        return True
    
    def execute(self, ctx):
        """Execute the task

        Args:
            ctx (any): Reserved parameters
        """
        return super().execute(ctx)
    