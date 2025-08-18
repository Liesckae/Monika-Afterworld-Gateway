import base


class TimeTrigger(base.Base):
    type = 'time trigger'
    
    def is_match(self, ctx):
        """Check if should execute

        Args:
            ctx (any): Reserved parameters

        Returns:
            bool: True if meet the condition; False if not
        """
        return super().is_match()
    
