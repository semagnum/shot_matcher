from .. import globalProps
from ..operators.CMA_OT_add_image_node import CMA_OT_add_image_node
from ..operators.CMA_OT_color_picker import CMA_OT_color_picker
from ..operators.CMA_OT_color_reset import CMA_OT_color_reset
from ..operators.CMA_OT_image_calculator import CMA_OT_image_calculator

import bpy

class CMA_PT_image_analyzer(bpy.types.Panel):
    bl_idname = "color_matching_analyzer.image_analyzer"
    bl_space_type = 'IMAGE_EDITOR'
    bl_label = "Color Matching"
    bl_category = "Color Matching"
    bl_region_type = 'UI'
    
    def draw(self, context):
        
        layout = self.layout
        
        split = layout.split()

        col = split.column()
        col.operator(CMA_OT_image_calculator.bl_idname, text = 'Calculate', icon='SEQ_HISTOGRAM')
        col = split.column(align=True)
        col.operator(CMA_OT_color_picker.bl_idname, text = 'Color Pick', icon='EYEDROPPER')
        col.operator(CMA_OT_color_reset.bl_idname, text = 'Reset Colors', icon='IMAGE_ALPHA')
        
        layout.operator(CMA_OT_add_image_node.bl_idname, text = 'Apply in Compositor', icon='NODETREE')
        
        layout.prop(context.scene, "max_color", text='White Color')
        layout.prop(context.scene, "min_color", text='Black Color')