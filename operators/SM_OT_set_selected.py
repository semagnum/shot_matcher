import bpy
from ..utils import get_layer_settings

class SM_OT_set_selected(bpy.types.Operator):
    bl_idname = 'shot_matcher.set_selected'
    bl_label = 'Use Current Media'
    bl_description = 'Sets the layer to the current image/video shown'
    bl_options = {'REGISTER'}

    space_type = bpy.props.StringProperty()

    @classmethod
    def poll(cls, context):
        return (hasattr(context, 'edit_image') and hasattr(context.edit_image, 'name')) or (hasattr(context, 'edit_movieclip') and hasattr(context.edit_movieclip, 'name'))
    
    def execute(self, context):
        media_name = ''
        if self.space_type == 'IMAGE_EDITOR':
            get_layer_settings(context).layer_name = context.edit_image.name
        elif self.space_type == 'CLIP_EDITOR':
            get_layer_settings(context).layer_name = context.edit_movieclip.name
        else:
            return {'CANCELLED'}

        return {'FINISHED'}
