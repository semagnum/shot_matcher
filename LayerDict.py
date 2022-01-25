import bpy
from .LayerSettings import LayerSettings


class LayerDict(bpy.types.PropertyGroup):
    name: bpy.props.StringProperty(name="Filename", default="Unknown")
    setting: bpy.props.PointerProperty(type=LayerSettings)
