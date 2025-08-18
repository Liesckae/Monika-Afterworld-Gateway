# -*- coding: utf-8 -*-
# 测试模块，用于调试和测试
from __future__ import print_function, unicode_literals
from mgr.modules.base import Base

class Test(Base):
    # 测试模块类
    name = 'test'
    desc = '测试模块'
    tags = ['test']
    triggers = []
    is_enable = True

    def execute(self, *args, **kwargs):
        # 执行测试逻辑
        import logging
        
        logging.getLogger('mgr').info('This is a fucking test message.')