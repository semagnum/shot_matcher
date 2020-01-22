import bpy

from ..operators.SM_OT_color_balance_node import SM_OT_color_balance_node
from ..operators.SM_OT_alpha_over_node import SM_OT_alpha_over_node
from ..operators.SM_OT_color_picker import SM_OT_color_picker
from ..operators.SM_OT_color_reset import SM_OT_color_reset
from ..operators.SM_OT_image_calculator import SM_OT_image_calculator
from ..operators.SM_OT_video_calculator import SM_OT_video_calculator
from ..operators.SM_OT_set_selected import SM_OT_set_selected

from ..utils import get_layer_settings

def draw_layer(itself, context, sm_layer):
    layout = itself.layout
    
    box = layout.box()
    
    box.row().prop(sm_layer, "layer_type", expand=True)
    
    if sm_layer.layer_type == 'video':
        box.prop_search(sm_layer, "layer_name", bpy.data, "movieclips", text='File', icon='FILE_MOVIE')
        if itself.bl_space_type == 'CLIP_EDITOR':
            box.operator(SM_OT_set_selected.bl_idname, text="Use Current Clip", icon='WINDOW').space_type = 'CLIP_EDITOR'
    else:
        box.prop_search(sm_layer, "layer_name", bpy.data, "images", text='File', icon='FILE_IMAGE')
        if itself.bl_space_type == 'IMAGE_EDITOR':
            box.operator(SM_OT_set_selected.bl_idname, text="Use Current Image", icon='WINDOW').space_type = 'IMAGE_EDITOR'
        
    box.prop(sm_layer, "use_alpha_threshold")
    if sm_layer.use_alpha_threshold:
        box.prop(sm_layer, "alpha_threshold", slider = True)
    
    box.row().prop(sm_layer, "max_color", text='White Color')
    box.row().prop(sm_layer, "min_color", text='Black Color')   
    
    col = box.column(align=True)
    if sm_layer.layer_type == 'image':
        if itself.bl_space_type == 'IMAGE_EDITOR':
            row = col.row(align=True)
            row.operator(SM_OT_color_picker.bl_idname, text="Color Pick", icon='EYEDROPPER')
            row.operator(SM_OT_color_reset.bl_idname, text="Reset Colors", icon='IMAGE_ALPHA')
        box.operator(SM_OT_image_calculator.bl_idname, text="Auto Calculate Colors", icon='SEQ_HISTOGRAM')
    else:
        col.prop(sm_layer, "start_frame", text='Start Frame')
        col.prop(sm_layer, "end_frame", text='End Frame')
        col.prop(sm_layer, "frame_step", text='Frame Step')
        col.operator(SM_OT_video_calculator.bl_idname, text="Auto Calculate Colors", icon='SEQ_HISTOGRAM')
    
        
def draw_panel(itself, context):
    layout = itself.layout
    scene = context.scene

    layout.prop(context.scene, 'layer_context', expand=True)
    
    draw_layer(itself, context, get_layer_settings(context)) 
        
    layout.label(text='Apply to Node Group:')
    
    layout.operator(SM_OT_color_balance_node.bl_idname, text="Color Balance", icon='COLOR')
    layout.operator(SM_OT_alpha_over_node.bl_idname, text="Alpha Over", icon='RENDERLAYERS')