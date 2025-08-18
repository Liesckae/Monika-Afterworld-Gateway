# -*- coding: utf-8 -*-
from __future__ import print_function, unicode_literals
import utils
import base

class DebugTrigger(base.Base):
    def is_match(self):
        return True