import bpy
from ..utils import frame_analyze

class SM_OT_image_calculator(bpy.types.Operator):
    bl_idname = "color_matching_analyzer.image_calculator"
    bl_label = "Image Color Analyzer"
    bl_description = "Calculates the maximum/minimum values for an image"
    bl_options = {'REGISTER'}

    layer = None
    
    @classmethod
    def poll(cls, context):
        return layer is not None and layer.layer_name
    
    def execute(self, context):
        
        context.window.cursor_set("WAIT")
          
        frame_analyze(context, bpy.data.images[layer.layer_name], True, layer)
        
        context.window.cursor_set("DEFAULT")
        return {'FINISHED'}