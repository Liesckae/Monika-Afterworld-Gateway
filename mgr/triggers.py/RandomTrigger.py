import base
import random

class RandomTrigger(base.Base):
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
        
    def is_match(self):
        """Check if should execute

        Returns:
            bool: True if meet the condition; False if not
        """
        return random.random() < self.probability

    