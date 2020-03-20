import bpy
from ..utils import frame_analyze, get_layer_settings
from ..LayerSettings import LayerSettings

class SM_OT_image_calculator(bpy.types.Operator):
    bl_idname = 'shot_matcher.image_calculator'
    bl_label = 'Image Color Analyzer'
    bl_description = 'Calculates the maximum/minimum values for an image'
    bl_options = {'REGISTER'}

    @classmethod
    def poll(cls, context):
        layer = get_layer_settings(context)
        return (layer.layer_name in bpy.data.images) and bpy.data.images[layer.layer_name].pixels
    
    def execute(self, context):
        context.window.cursor_set('WAIT')

        frame_analyze(context, bpy.data.images[get_layer_settings(context).layer_name], True)
        
        context.window.cursor_set('DEFAULT')
        return {'FINISHED'}