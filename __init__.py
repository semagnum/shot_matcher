'''

Created by Spencer Magnusson
semagnum+blendermarket@gmail.com

'''

bl_info = {
    "name": 'Shot Matcher',
    "author": 'Spencer Magnusson',
    "version": (3, 2, 0),
    "blender": (2, 80, 0),
    "description": 'Analyzes colors of an image or movie clip and applies it to the compositing tree.',
    "location": 'Image Editor > UI > Shot Matcher & Movie Clip Editor > Tools > Shot Matcher',
    "support": 'COMMUNITY',
    "category": 'Compositing'
}

import bpy

from . import auto_load
from .LayerSettings import LayerSettings
from .LayerDict import LayerDict
from .utils import update_layer_link, type_update

auto_load.init()

def register():
    auto_load.register()
    scene = bpy.types.Scene
    scene.sm_settings_movieclips = bpy.props.CollectionProperty(type=LayerDict)
    scene.sm_settings_images = bpy.props.CollectionProperty(type=LayerDict)
    scene.sm_fg_type: bpy.props.EnumProperty(
        name='Layer Type',
        description='Select which file type the foreground layer is',
        items=[ ('video', 'Video','', 'FILE_MOVIE', 1),
                ('image', 'Image','', 'FILE_IMAGE', 2),
               ]
        update=type_update
        )
    scene.sm_bg_type: bpy.props.EnumProperty(
        name='Layer Type',
        description='Select which file type the background layer is',
        items=[ ('video', 'Video','', 'FILE_MOVIE', 1),
                ('image', 'Image','', 'FILE_IMAGE', 2),
               ],
        update=type_update
        )
    scene.layer_context = bpy.props.EnumProperty(
        name='Layer',
        description='The current layer being analyzed',
        items=[ ('bg', 'Background', ''),
                ('fg', 'Foreground', ''),
               ]
        )
    scene.sm_background = bpy.props.PointerProperty(type=LayerSettings)
    scene.sm_foreground = bpy.props.PointerProperty(type=LayerSettings)
    scene.sm_bg_name = bpy.props.StringProperty(update=update_layer_link)
    scene.sm_fg_name = bpy.props.StringProperty(update=update_layer_link)

def unregister():
    auto_load.unregister()
    scene = bpy.types.Scene
    del  scene.sm_settings_movieclips, scene.sm_settings_images, scene.sm_bg_type, scene.sm_fg_type, scene.sm_background, scene.sm_foreground, scene.layer_context
