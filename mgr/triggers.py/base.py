import utils
m_logger = utils.get_default_logger()

class Base:
    def __init__(self, name=None, desc=None):
        self.name = name
        self.desc = desc
    def is_match(self):
        pass
    