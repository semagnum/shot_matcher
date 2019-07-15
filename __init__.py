'''

Created by Spencer Magnusson
semagnum+blendermarket@gmail.com

'''

bl_info = {
    "name": "Color Matching Analyzer",
    "author": "Spencer Magnusson",
    "version": (2, 0, 0),
    "blender": (2, 79, 0),
    "description": "Analyzes colors of an image or movie clip and applies it to the compositing tree.",
    "location": "Image Editor > UI > Color Matching & Movie Clip Editor > Tools > Color Matching",
    "support": "COMMUNITY",
    "category": "Compositing"
}

import bpy


# load and reload submodules
##################################

import importlib
from . import developer_utils
importlib.reload(developer_utils)
modules = developer_utils.setup_addon_modules(__path__, __name__, "bpy" in locals())


# register
##################################

import traceback

def register():
    try: bpy.utils.register_module(__name__)
    except: traceback.print_exc()

    print("Registered {} with {} modules".format(bl_info["name"], len(modules)))

def unregister():
    try: bpy.utils.unregister_module(__name__)
    except: traceback.print_exc()

    print("Unregistered {}".format(bl_info["name"]))
