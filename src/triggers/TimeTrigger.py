import base
from src.utils.logger import m_logger

class TimeTrigger(base.TriggerBase):
    type = 'time trigger'
    
    def check(self, ctx):
        """Check if should execute

        Args:
            ctx (any): Reserved parameters

        Returns:
            bool: True if meet the condition; False if not
        """
        return super().check(ctx)
    
    def execute(self, ctx):
        """Execute the task

        Args:
            ctx (any): Reserved parameters
        """
        super().execute(ctx)