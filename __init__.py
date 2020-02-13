'''

Created by Spencer Magnusson
semagnum+blendermarket@gmail.com

'''

bl_info = {
    "name": 'Shot Matcher',
    "author": 'Spencer Magnusson',
    "version": (3, 1, 1),
    "blender": (2, 80, 0),
    "description": 'Analyzes colors of an image or movie clip and applies it to the compositing tree.',
    "location": 'Image Editor > UI > Shot Matcher & Movie Clip Editor > Tools > Shot Matcher',
    "support": 'COMMUNITY',
    "category": 'Compositing'
}

import bpy

from . import auto_load
from .LayerSettings import LayerSettings

auto_load.init()

def register():
    auto_load.register()
    scene = bpy.types.Scene
    scene.layer_context = bpy.props.EnumProperty(
        name='Layer',
        description='The current layer being analyzed',
        items=[ ('bg', 'Background', ''),
                ('fg', 'Foreground', ''),
               ]
        )
    scene.sm_background = bpy.props.PointerProperty(type=LayerSettings)
    scene.sm_foreground = bpy.props.PointerProperty(type=LayerSettings)

def unregister():
    auto_load.unregister()
    scene = bpy.types.Scene
    del scene.sm_background, scene.sm_foreground, scene.layer_context
