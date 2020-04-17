'''
Created by Spencer Magnusson
semagnum+blendermarket@gmail.com
'''

bl_info = {
    "name": 'Shot Matcher',
    "author": 'Spencer Magnusson',
    "version": (3, 3, 0),
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
from .utils import type_update, get_bg_name, get_fg_name, set_bg_name, set_fg_name, copy_settings
from bpy.app.handlers import persistent

auto_load.init()

@persistent
def save_pre_layer_settings(dummy):
    def save_layer(scene, layer_name, sm_layer, sm_layer_type):
        if layer_name == '':
            return
        
        if sm_layer_type == 'video':
            layer_dict = scene.sm_settings_movieclips
        else:
            layer_dict = scene.sm_settings_images
        
        current_index = layer_dict.find(layer_name)
        copy_settings(sm_layer, layer_dict[current_index].setting)
    for scene in bpy.data.scenes:
    	save_layer(scene, scene.sm_bg_name, scene.sm_background, scene.sm_bg_type)
    	save_layer(scene, scene.sm_fg_name, scene.sm_foreground, scene.sm_fg_type)

@persistent
def load_post_purge_settings(dummy):
    def purge_layer(settings_list, data_list, print_type):
        index = 0
        nameList = []
        while index < len(settings_list):
            if settings_list[index].name not in data_list:
                nameList.append(settings_list[index].name)
                settings_list.remove(index)
            else:
                index +=1
        if len(nameList) > 0:
            print('{} layer settings have been removed for the following {}:'.format(len(nameList), print_type))
            for name in nameList:
                print('\t{}'.format(name))
    for scene in bpy.data.scenes:
    	purge_layer(scene.sm_settings_movieclips, bpy.data.movieclips, 'movieclips')
    	purge_layer(scene.sm_settings_images, bpy.data.images, 'images')

def register():
    auto_load.register()
    scene = bpy.types.Scene
    scene.sm_settings_movieclips = bpy.props.CollectionProperty(type=LayerDict)
    scene.sm_settings_images = bpy.props.CollectionProperty(type=LayerDict)
    scene.sm_fg_type = bpy.props.EnumProperty(
        name='Layer Type',
        description='Select which file type the foreground layer is',
        items=[ ('video', 'Video','', 'FILE_MOVIE', 1),
                ('image', 'Image','', 'FILE_IMAGE', 2),
               ],
        update=type_update
        )
    scene.sm_bg_type = bpy.props.EnumProperty(
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
    scene.sm_bg_name = bpy.props.StringProperty(default='', get=get_bg_name, set=set_bg_name)
    scene.sm_fg_name = bpy.props.StringProperty(default='', get=get_fg_name, set=set_fg_name)

    bpy.app.handlers.save_pre.append(save_pre_layer_settings)
    bpy.app.handlers.load_post.append(load_post_purge_settings)

def unregister():
    auto_load.unregister()
    scene = bpy.types.Scene
    del scene.sm_settings_movieclips, scene.sm_settings_images, scene.sm_bg_type, scene.sm_fg_type, scene.sm_background, scene.sm_foreground, scene.layer_context
    bpy.app.handlers.save_pre.remove(save_pre_layer_settings)
    bpy.app.handlers.load_post.remove(load_post_purge_settings)
