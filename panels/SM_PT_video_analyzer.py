import bpy
from ..LayerSettings import LayerSettings

class SM_PT_video_analyzer(bpy.types.Panel):
    bl_space_type = 'CLIP_EDITOR'
    bl_label = "Shot Matcher"
    bl_category = "Shot Matcher"
    bl_region_type = 'TOOLS'
    
    def draw(self, context):
        LayerSettings.draw_panel(self, context)
