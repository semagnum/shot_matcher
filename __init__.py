'''

Created by Spencer Magnusson
semagnum+blendermarket@gmail.com

'''

bl_info = {
    "name": "Color Matching Analyzer",
    "author": "Spencer Magnusson",
    "version": (2, 0, 0),
    "blender": (2, 80, 0),
    "description": "Analyzes colors of an image or movie clip and applies it to the compositing tree.",
    "location": "Image Editor > UI > Color Matching & Movie Clip Editor > Tools > Color Matching",
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
