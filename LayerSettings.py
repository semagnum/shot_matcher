import bpy

class LayerSettings(bpy.types.PropertyGroup):
    
    def type_update(self, context):
        self.layer_name = ''
    
    max_color: bpy.props.FloatVectorProperty(
        description='The color representing the white value of this layer',
        default=(1.0, 1.0, 1.0),
        min=0.0,
        precision=4,
        subtype='COLOR')
    min_color: bpy.props.FloatVectorProperty(
        description='The color representing the black value of this layer',
        default=(0.0, 0.0, 0.0),
        min=0.0,
        precision=4,
        subtype='COLOR')
        
    layer_name: bpy.props.StringProperty(description='Name of the file to use for this layer')
        
    layer_type: bpy.props.EnumProperty(
        name='Layer Type',
        description='Select which file type the layer is',
        items=[ ('video', 'Video','', 'FILE_MOVIE', 1),
                ('image', 'Image','', 'FILE_IMAGE', 2),
               ],
        update=type_update
        )
        
    use_alpha_threshold: bpy.props.BoolProperty(default=False,name='Use Alpha Threshold')
    alpha_threshold: bpy.props.FloatProperty(name='Alpha Threshold',
        description='Threshold of an alpha value for having its pixel considered for analysis',
        default=0.75, min=0.0, max=1.0,
        step=5, precision=2)
    
    start_frame: bpy.props.IntProperty(default=1)
    end_frame: bpy.props.IntProperty(default=250)
    frame_step: bpy.props.IntProperty(
        default=10,
        min=1)