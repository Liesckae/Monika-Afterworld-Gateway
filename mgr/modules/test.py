# -*- coding: utf-8 -*-
from __future__ import print_function, unicode_literals
from mgr.modules.base import Base

class Test(Base):
    name = 'test'
    desc = '测试模块'
    tags = ['test']
    triggers = []
    is_enable = True

    def execute(self, *args, **kwargs):
        import logging
        
        logging.getLogger('mgr').info('This is a fucking test message.')