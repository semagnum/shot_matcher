from .layer_base import BaseLayer


class SourceLayer(BaseLayer):

    def __init__(self, context):
        self.layer_type = 'source'
        self.media_type = context.scene.sm_fg_type
        self.media_type_str = 'sm_fg_type'
        self.name = context.scene.sm_fg_name
        self.name_str = 'sm_fg_name'
        self.settings = context.scene.sm_foreground
        self.settings_name = 'sm_foreground'
