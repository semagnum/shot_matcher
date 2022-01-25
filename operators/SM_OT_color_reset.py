import bpy

from ..utils import get_layer_settings


class SM_OT_color_reset(bpy.types.Operator):
    bl_idname = 'shot_matcher.color_reset'
    bl_label = 'Reset Min and Max Colors'
    bl_description = 'Resets the maximum and minimum color values for use with the color picker'
    bl_options = {'REGISTER', 'UNDO'}
    
    def execute(self, context):
        context_layer = get_layer_settings(context)
        max_color = (10000.0, 10000.0, 10000.0)
        min_color = (0.0, 0.0, 0.0)
        context_layer.max_color = min_color
        context_layer.min_color = max_color
        return {'FINISHED'}
