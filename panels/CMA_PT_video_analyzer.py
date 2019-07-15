from ..operators.CMA_OT_video_calculator import CMA_OT_video_calculator
from ..operators.CMA_OT_add_video_node import CMA_OT_add_video_node

import bpy

class CMA_PT_video_analyzer(bpy.types.Panel):
    bl_idname = "color_matching_analyzer.video_analyzer"
    bl_space_type = 'CLIP_EDITOR'
    bl_label = "Color-Matching Analyzer"
    bl_category = "Color-Matching"
    bl_region_type = 'TOOLS'
    
    def draw(self, context):

        layout = self.layout

        layout.operator(CMA_OT_video_calculator.bl_idname, text = 'Calculate', icon='SEQ_HISTOGRAM')
        layout.operator(CMA_OT_add_video_node.bl_idname, text = 'Apply in Compositor', icon='NODETREE')
        
        layout.prop(context.scene, "max_color", text='White Color')
        layout.prop(context.scene, "min_color", text='Black Color')

        col = layout.column(align=True)
        col.label(text="Frame Range:")
        col.prop(context.scene, "cma_start_frame", text='Start Frame')
        col.prop(context.scene, "cma_end_frame", text='End Frame')
        col.prop(context.scene, "cma_frame_step", text='Frame Step')