import bpy, sys

class CMA_OT_color_reset(bpy.types.Operator):
    bl_idname = "color_matching_analyzer.color_reset"
    bl_label = "Reset Min and Max Colors"
    bl_options = {'REGISTER', 'UNDO'}
    
    def execute(self, context):
        max_color = (10000.0, 10000.0, 10000.0)
        min_color = (0.0, 0.0, 0.0)
        context.scene.max_color = min_color
        context.scene.min_color = max_color
        return {'FINISHED'}