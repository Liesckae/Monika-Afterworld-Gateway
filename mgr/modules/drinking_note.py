from __future__ import print_function, unicode_literals
from mgr.modules.base import Base
import mgr.triggers.debugtrigger as debugtrigger

class Test(Base):
    # 测试模块类
    name = u'喝水提醒'
    desc = u'提醒你该喝水了！'
    tags = [u'test']
    triggers = [debugtrigger.DebugTrigger()]
    is_enable = False

    def execute(self, *args, **kwargs):
        # 执行测试逻辑
        import io
        with io.open('C:\\Users\\admin\\Desktop\\note.txt', 'w', encoding='utf-8') as f:
            f.write(u'记得准时喝水！ ——爱你的Monika\n')