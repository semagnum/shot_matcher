import bpy
from ..utils import frame_analyze, get_layer_settings
from ..LayerSettings import LayerSettings

class SM_OT_image_calculator(bpy.types.Operator):
    bl_idname = "shot_matcher.image_calculator"
    bl_label = "Image Color Analyzer"
    bl_description = "Calculates the maximum/minimum values for an image"
    bl_options = {'REGISTER'}

    @classmethod
    def poll(cls, context):
       return bpy.data.images[get_layer_settings(context).layer_name] is not None
    
    def execute(self, context):
        context.window.cursor_set("WAIT")

        context_layer = get_layer_settings(context)
        frame_analyze(context, bpy.data.images[context_layer.layer_name], True)
        
        context.window.cursor_set("DEFAULT")
        return {'FINISHED'}