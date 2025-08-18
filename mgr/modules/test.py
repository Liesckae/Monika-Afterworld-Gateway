# -*- coding: utf-8 -*-
from __future__ import print_function, unicode_literals
import utils
import base

class Test(base.Base):
    name = 'test_module'
    desc = '这是一个测试模块'
    tags = ['test']
    topics = []
    triggers = ['test_trigger']
    
    def __init__(self):
        super(base.Base, self).__init__()
        
    def execute(self):
        utils.get_default_logger().info("test module executed")