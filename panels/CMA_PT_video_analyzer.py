from ..operators.CMA_OT_video_calculator import CMA_OT_video_calculator
from ..operators.CMA_OT_add_video_node import CMA_OT_add_video_node

import bpy

class CMA_PT_video_analyzer(bpy.types.Panel):
    bl_space_type = 'CLIP_EDITOR'
    bl_label = "Movie Clip Analyzer"
    bl_category = "Shot Matcher"
    bl_region_type = 'TOOLS'
    
    def draw(self, context):

        layout = self.layout

        layout.label(text="Automatic Calculation")
        layout.operator(CMA_OT_video_calculator.bl_idname, text = 'Calculate Colors', icon='SEQ_HISTOGRAM')

        col = layout.column(align=True)
        col.prop(context.scene, "cma_start_frame", text='Start Frame')
        col.prop(context.scene, "cma_end_frame", text='End Frame')
        col.prop(context.scene, "cma_frame_step", text='Frame Step')

        layout.prop(context.scene, "sm_use_alpha_threshold")
        if context.scene.sm_use_alpha_threshold:
            layout.prop(context.scene, "sm_alpha_threshold", slider = True)

        layout.label(text="Apply")
        layout.operator(CMA_OT_add_video_node.bl_idname, text = 'Apply in Compositor', icon='NODETREE')
