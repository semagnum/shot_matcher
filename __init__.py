'''

Created by Spencer Magnusson
semagnum+blendermarket@gmail.com

'''

bl_info = {
    "name": "Shot Matcher",
    "author": "Spencer Magnusson",
    "version": (2, 2, 0),
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

def unregister():
    auto_load.unregister()
