import bpy

bpy.types.Scene.min_color = bpy.props.FloatVectorProperty(
    default=(0.0, 0.0, 0.0),
    min=0.0,
    precision=4,
    subtype='COLOR')
bpy.types.Scene.max_color = bpy.props.FloatVectorProperty(
    default=(1.0, 1.0, 1.0),
    min=0.0,
    precision=4,
    subtype='COLOR')

bpy.types.Scene.cma_start_frame = bpy.props.IntProperty(
    default=1)
bpy.types.Scene.cma_end_frame = bpy.props.IntProperty(
    default=250)
bpy.types.Scene.cma_frame_step = bpy.props.IntProperty(
    default=10,
    min=1)

bpy.types.Scene.sm_use_alpha_threshold = bpy.props.BoolProperty(name="Use Alpha Threshold")
bpy.types.Scene.sm_alpha_threshold = bpy.props.FloatProperty(name="Alpha Threshold", description="Threshold of an alpha value for having its pixel considered for analysis", default=0.75, min=0.0, max=1.0, step=5, precision=2)
