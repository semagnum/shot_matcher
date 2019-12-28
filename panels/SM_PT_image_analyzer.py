import bpy

from ..LayerSettings import LayerSettings

class SM_PT_image_analyzer(bpy.types.Panel):
    bl_space_type = 'IMAGE_EDITOR'
    bl_label = "Shot Matcher"
    bl_category = "Shot Matcher"
    bl_region_type = 'UI'
    
    def draw(self, context):
        LayerSettings.draw_panel(self, context)
