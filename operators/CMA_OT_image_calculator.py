import bpy
from ..utils import frame_analyze

class CMA_OT_image_calculator(bpy.types.Operator):
    bl_idname = "color_matching_analyzer.image_calculator"
    bl_label = "Image Color Analyzer"
    bl_options = {'REGISTER'}
    
    @classmethod
    def poll(cls, context):
        return context.edit_image is not None and context.edit_image.pixels
    
    def execute(self, context):
        
        context.window.cursor_set("WAIT")
          
        frame_analyze(context, context.edit_image, True)
        
        context.window.cursor_set("DEFAULT")        
        return {'FINISHED'}