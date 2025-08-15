import base
from src.utils.logger import m_logger
import random

class RandomTrigger(base.TriggerBase):
    type = 'Random Trigger'
    
    def __init__(self, name, desc='', probability=0):
        """Initialize when the subclass is instantiates

        Args:
            name (str): The name of the instance
            desc (str, optional): Description of this instance. Defaults to ''.
            probability (int, optional): The probability (0 - 1.0) that the trigger should execute.Defaults to 0.
        """
        super().__init__(name, desc)
        self.probability = probability
        
    def check(self, ctx):
        """Check if should execute

        Args:
            ctx (any): Reserved parameters

        Returns:
            bool: True if meet the condition; False if not
        """
        return random.random() < self.probability
    
    def execute(self, ctx):
        """Execute the task

        Args:
            ctx (any): Reserved parameters
        """
        super().execute(ctx)
    