import bpy

class LayerSettings(bpy.types.PropertyGroup):
    
    def type_update(self, context):
        self.layer_name = ''
    
    max_color: bpy.props.FloatVectorProperty(
        description="The color representing the white value of this layer",
        default=(1.0, 1.0, 1.0),
        min=0.0,
        precision=4,
        subtype='COLOR')
    min_color: bpy.props.FloatVectorProperty(
        description="The color representing the black value of this layer",
        default=(0.0, 0.0, 0.0),
        min=0.0,
        precision=4,
        subtype='COLOR')
        
    layer_name: bpy.props.StringProperty(description="Name of the file to use for this layer")
        
    layer_type: bpy.props.EnumProperty(
        name="Layer Type",
        description="Select which file type the layer is",
        items=[ ('video', "Video",'', 'FILE_MOVIE', 1),
                ('image', "Image",'', 'FILE_IMAGE', 2),
               ],
        update=type_update
        )
        
    use_alpha_threshold: bpy.props.BoolProperty(default=False,name="Use Alpha Threshold")
    alpha_threshold: bpy.props.FloatProperty(name="Alpha Threshold",
        description="Threshold of an alpha value for having its pixel considered for analysis",
        default=0.75, min=0.0, max=1.0,
        step=5, precision=2)
    
    start_frame: bpy.props.IntProperty(default=1)
    end_frame: bpy.props.IntProperty(default=250)
    frame_step: bpy.props.IntProperty(
        default=10,
        min=1)
        
    def draw_layer(itself, context, sm_layer):
        layout = itself.layout
        
        box = layout.box()
        
        box.row().prop(sm_layer, "layer_type", expand=True)
        
        if sm_layer.layer_type == 'video':
            box.prop_search(sm_layer, "layer_name", bpy.data, "movieclips", text='File', icon='FILE_MOVIE')
            if itself.bl_space_type == 'CLIP_EDITOR':
                box.operator("object.select_all", text="Use Current Clip", icon='WINDOW')
        else:
            box.prop_search(sm_layer, "layer_name", bpy.data, "images", text='File', icon='FILE_IMAGE')
            if itself.bl_space_type == 'IMAGE_EDITOR':
                box.operator("object.select_all", text="Use Current Image", icon='WINDOW')
            
        box.prop(sm_layer, "use_alpha_threshold")
        if sm_layer.use_alpha_threshold:
            box.prop(sm_layer, "alpha_threshold", slider = True)
        
        box.row().prop(sm_layer, "max_color", text='White Color')
        box.row().prop(sm_layer, "min_color", text='Black Color')   
        
        col = box.column(align=True)
        if sm_layer.layer_type == 'image':
            row = col.row(align=True)
            row.operator("object.select_all", text="Color Pick", icon='EYEDROPPER').layer = sm_layer
            row.operator(SM_OT_color_reset.bl_idname, text="Reset Colors", icon='IMAGE_ALPHA').layer = sm_layer
            box.operator(SM_OT_image_calculator.bl_idname, text="Auto Calculate Colors", icon='SEQ_HISTOGRAM').layer = sm_layer
        else:
            col.prop(sm_layer, "start_frame", text='Start Frame')
            col.prop(sm_layer, "end_frame", text='End Frame')
            col.prop(sm_layer, "frame_step", text='Frame Step')
            col.operator(SM_OT_video_calculator.bl_idname, text="Auto Calculate Colors", icon='SEQ_HISTOGRAM').layer = sm_layer
      
            
    def draw_panel(itself, context):
        layout = itself.layout
        scene = context.scene
        layout.prop(scene, "show_bg_options", icon="DOWNARROW_HLT" if scene.show_bg_options else "RIGHTARROW", text="Background", emboss=False)
        
        if scene.show_bg_options:
            LayerSettings.draw_layer(itself, context, context.scene.sm_background) 
        
        layout.prop(scene, "show_fg_options", icon="DOWNARROW_HLT" if scene.show_fg_options else "RIGHTARROW", text="Foreground", emboss=False)
        
        if scene.show_fg_options:
            LayerSettings.draw_layer(itself, context, context.scene.sm_foreground)
            
        layout.label(text='Apply to Node Group:')
        
        layout.operator("object.select_all", text="Color Balance", icon='COLOR')
        layout.operator("object.select_all", text="Alpha Over", icon='RENDERLAYERS')