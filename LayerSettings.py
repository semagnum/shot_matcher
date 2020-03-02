import bpy

def copy_settings(first_layer, second_layer):
    second_layer.max_color = first_layer.max_color
    second_layer.min_color = first_layer.min_color
    second_layer.use_alpha_threshold = first_layer.use_alpha_threshold
    second_layer.alpha_threshold = first_layer.alpha_threshold
    second_layer.start_frame = first_layer.start_frame
    second_layer.end_frame = first_layer.end_frame
    second_layer.frame_step = first_layer.frame_step

class LayerSettings(bpy.types.PropertyGroup):
    
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