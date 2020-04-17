import bpy
from ..utils import get_layer_name
from .op_utils import frame_analyze

class SM_OT_image_calculator(bpy.types.Operator):
    bl_idname = 'shot_matcher.image_calculator'
    bl_label = 'Image Color Analyzer'
    bl_description = 'Calculates the maximum/minimum values for an image'
    bl_options = {'REGISTER'}

    @classmethod
    def poll(cls, context):
        layer = get_layer_name(context)
        return (layer in bpy.data.images) and bpy.data.images[layer].pixels
    
    def execute(self, context):
        context.window.cursor_set('WAIT')

        frame_analyze(context, bpy.data.images[get_layer_name(context)], True)
        
        context.window.cursor_set('DEFAULT')
        return {'FINISHED'}