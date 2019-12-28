'''

Created by Spencer Magnusson
semagnum+blendermarket@gmail.com

'''

bl_info = {
    "name": "Shot Matcher",
    "author": "Spencer Magnusson",
    "version": (3, 0, 0),
    "blender": (2, 80, 0),
    "description": "Analyzes colors of an image or movie clip and applies it to the compositing tree.",
    "location": "Image Editor > UI > Shot Matcher & Movie Clip Editor > Tools > Shot Matcher",
    "support": "COMMUNITY",
    "category": "Compositing"
}

import bpy

from . import auto_load

auto_load.init()

def register():
    auto_load.register()
    scene = bpy.types.Scene
    scene.show_bg_options = bpy.props.BoolProperty(default=True)
    scene.show_fg_options = bpy.props.BoolProperty(default=True)
    scene.sm_background = bpy.props.PointerProperty(type=LayerSettings)
    scene.sm_foreground = bpy.props.PointerProperty(type=LayerSettings)

def unregister():
    auto_load.unregister()
    scene = bpy.types.Scene
    del scene.sm_background, scene.sm_foreground, scene.show_bg_options, scene.show_fg_options
