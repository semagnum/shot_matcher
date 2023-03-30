class BaseLayer:

    def __init__(self, _context):
        self.layer_type = ''
        self.media_type = None
        self.media_type_str = ''
        self.name = None
        self.name_str = ''
        self.settings = None
        self.settings_name = ''

    def type_update(self):
        self.name = ''
