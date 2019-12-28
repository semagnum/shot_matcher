import bpy, sys

class SM_OT_color_reset(bpy.types.Operator):
    bl_idname = "color_matching_analyzer.color_reset"
    bl_label = "Reset Min and Max Colors"
    bl_description = "Resets the maximum and minimum color values for use with the color picker"
    bl_options = {'REGISTER', 'UNDO'}

    layer = None
    
    def execute(self, context):
        max_color = (10000.0, 10000.0, 10000.0)
        min_color = (0.0, 0.0, 0.0)
        layer.max_color = min_color
        layer.min_color = max_color
        return {'FINISHED'}
