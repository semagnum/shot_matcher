import bpy
from .panel_utils import draw_panel


class SM_PT_video_analyzer(bpy.types.Panel):
    bl_space_type = 'CLIP_EDITOR'
    bl_label = "Shot Matcher"
    bl_category = "Shot Matcher"
    bl_region_type = 'TOOLS'

    def draw(self, context):
        draw_panel(self, context)
