import bpy
from ..utils import get_layer_settings, valid_video_layer, valid_image_layer

class SM_OT_set_selected(bpy.types.Operator):
    bl_idname = 'shot_matcher.set_selected'
    bl_label = 'Use Current Media'
    bl_description = 'Sets the layer to the current image/video shown'
    bl_options = {'REGISTER'}

    space_type = bpy.props.StringProperty()

    @classmethod
    def poll(cls, context):
        current_layer = get_layer_settings(context)
        return (current_layer.layer_type == 'video' and valid_video_layer(current_layer)) or valid_image_layer(current_layer)
    
    def execute(self, context):
        media_name = ''
        if self.space_type == 'IMAGE_EDITOR':
            get_layer_settings(context).layer_name = context.edit_image.name
        elif self.space_type == 'CLIP_EDITOR':
            get_layer_settings(context).layer_name = context.edit_movieclip.name
        else:
            return {'CANCELLED'}

        return {'FINISHED'}