# -*- coding: utf-8 -*-
from __future__ import print_function, unicode_literals
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
        return super(base.Base, self).__init__()
    
