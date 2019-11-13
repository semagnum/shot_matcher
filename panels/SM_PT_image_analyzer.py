from .. import globalProps
from ..operators.SM_OT_add_image_node import SM_OT_add_image_node
from ..operators.SM_OT_color_picker import SM_OT_color_picker
from ..operators.SM_OT_color_reset import SM_OT_color_reset
from ..operators.SM_OT_image_calculator import SM_OT_image_calculator

import bpy

class SM_PT_image_analyzer(bpy.types.Panel):
    bl_space_type = 'IMAGE_EDITOR'
    bl_label = "Image Analysis"
    bl_category = "Shot Matcher"
    bl_region_type = 'UI'
    
    def draw(self, context):
        
        layout = self.layout
        
        layout.label(text="Automatic Calculation")

        layout.operator(SM_OT_image_calculator.bl_idname, text = 'Calculate Colors', icon='SEQ_HISTOGRAM')
        layout.prop(context.scene, "sm_use_alpha_threshold")
        if context.scene.sm_use_alpha_threshold:
            layout.prop(context.scene, "sm_alpha_threshold", slider = True)
        
        layout.label(text="Color Picker")
        layout.operator(SM_OT_color_picker.bl_idname, text = 'Color Pick', icon='EYEDROPPER')
        layout.operator(SM_OT_color_reset.bl_idname, text = 'Reset Colors', icon='IMAGE_ALPHA')

        layout.prop(context.scene, "max_color", text='White Color')
        layout.prop(context.scene, "min_color", text='Black Color')
        
        layout.label(text="Apply")
        layout.operator(SM_OT_add_image_node.bl_idname, text = 'Apply in Compositor', icon='NODETREE')
