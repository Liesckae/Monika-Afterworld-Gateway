import utils
m_logger = utils.get_default_logger()

class Base:
    def __init__(self, name=None):
        self.name = name
        
    def is_match(self):
        pass
    