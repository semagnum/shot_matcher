from .layer_base import BaseLayer


class TargetLayer(BaseLayer):

    def __init__(self, context):
        self.layer_type = 'target'
        self.media_type = context.scene.sm_bg_type
        self.media_type_str = 'sm_bg_type'
        self.name = context.scene.sm_bg_name
        self.name_str = 'sm_bg_name'
        self.settings = context.scene.sm_background
        self.settings_name = 'sm_background'
