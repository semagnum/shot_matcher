from .. import globalProps
from ..operators.CMA_OT_add_image_node import CMA_OT_add_image_node
from ..operators.CMA_OT_color_picker import CMA_OT_color_picker
from ..operators.CMA_OT_color_reset import CMA_OT_color_reset
from ..operators.CMA_OT_image_calculator import CMA_OT_image_calculator

import bpy

class CMA_PT_image_analyzer(bpy.types.Panel):
    bl_space_type = 'IMAGE_EDITOR'
    bl_label = "Image Analysis"
    bl_category = "Shot Matcher"
    bl_region_type = 'UI'
    
    def draw(self, context):
        
        layout = self.layout
        
        layout.label(text="Automatic Calculation")

        layout.operator(CMA_OT_image_calculator.bl_idname, text = 'Calculate Colors', icon='SEQ_HISTOGRAM')
        
        layout.label(text="Color Picker")
        layout.operator(CMA_OT_color_picker.bl_idname, text = 'Color Pick', icon='EYEDROPPER')
        layout.operator(CMA_OT_color_reset.bl_idname, text = 'Reset Colors', icon='IMAGE_ALPHA')
        
        layout.label(text="Apply to Compositor")
        layout.operator(CMA_OT_add_image_node.bl_idname, text = 'Update Node Group', icon='NODETREE')
        
        layout.prop(context.scene, "sm_use_alpha_threshold")
        if context.scene.sm_use_alpha_threshold:
            layout.prop(context.scene, "sm_alpha_threshold")
        
        layout.prop(context.scene, "max_color", text='White Color')
        layout.prop(context.scene, "min_color", text='Black Color')
