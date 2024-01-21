"""
Copyright (C) 2024 Spencer Magnusson
semagnum@gmail.com
Created by Spencer Magnusson
    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.
    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.
    You should have received a copy of the GNU General Public License
    along with this program.  If not, see <http://www.gnu.org/licenses/>.
"""

if "bpy" in locals():
    import importlib
    import os
    import types

    # double-check this add-on is imported, so it can be referenced and reloaded
    import shot_matcher

    def reload_package(package):
        assert (hasattr(package, '__package__'))
        fn = package.__file__
        fn_dir = os.path.dirname(fn) + os.sep
        module_visit = {fn}
        del fn

        def reload_recursive_ex(module):
            module_iter = (
                module_child
                for module_child in vars(module).values()
                if isinstance(module_child, types.ModuleType)
            )
            for module_child in module_iter:
                fn_child = getattr(module_child, '__file__', None)
                if (fn_child is not None) and fn_child.startswith(fn_dir) and fn_child not in module_visit:
                    module_visit.add(fn_child)
                    reload_recursive_ex(module_child)

            importlib.reload(module)

            print('Reloaded', module.__name__)

        return reload_recursive_ex(package)

    reload_package(shot_matcher)

import bpy

from . import operators, panels

from .handlers import set_bg_name, set_fg_name, get_bg_name, get_fg_name, bg_update, fg_update
from .handlers import save_pre_layer_settings, load_post_purge_settings
from .layers import LayerSettings, LayerDict

bl_info = {
    "name": 'Shot Matcher',
    "author": 'Spencer Magnusson',
    "version": (3, 5, 4),
    "blender": (4, 0, 0),
    "description": 'Analyzes colors of an image or movie clip and applies it to the compositing tree.',
    "location": 'Image Editor > UI > Shot Matcher, Movie Clip Editor > Tools > Shot Matcher, Compositor > UI > Shot Matcher',
    "support": 'COMMUNITY',
    "category": 'Compositing',
    'doc_url': 'https://semagnum.github.io/shot-matcher/',
    'tracker_url': 'https://github.com/semagnum/shot-matcher/issues',
}

MODEL_CLASSES = (LayerSettings, LayerDict)


def register():
    for cls in MODEL_CLASSES:
        bpy.utils.register_class(cls)

    scene = bpy.types.Scene
    scene.sm_settings_movieclips = bpy.props.CollectionProperty(type=LayerDict)
    scene.sm_settings_images = bpy.props.CollectionProperty(type=LayerDict)
    scene.sm_fg_type = bpy.props.EnumProperty(
        name='Layer Type',
        description='Select which file type the foreground layer is',
        items=[('video', 'Video', '', 'FILE_MOVIE', 1),
               ('image', 'Image', '', 'FILE_IMAGE', 2),
               ],
        update=fg_update
    )
    scene.sm_bg_type = bpy.props.EnumProperty(
        name='Layer Type',
        description='Select which file type the background layer is',
        items=[('video', 'Video', '', 'FILE_MOVIE', 1),
               ('image', 'Image', '', 'FILE_IMAGE', 2),
               ],
        update=bg_update
    )

    scene.sm_background = bpy.props.PointerProperty(type=LayerSettings)
    scene.sm_foreground = bpy.props.PointerProperty(type=LayerSettings)
    scene.sm_bg_name = bpy.props.StringProperty(default='', get=get_bg_name, set=set_bg_name)
    scene.sm_fg_name = bpy.props.StringProperty(default='', get=get_fg_name, set=set_fg_name)

    bpy.app.handlers.save_pre.append(save_pre_layer_settings)
    bpy.app.handlers.load_post.append(load_post_purge_settings)

    operators.register()
    panels.register()


def unregister():
    panels.unregister()
    operators.unregister()
    scene = bpy.types.Scene

    bpy.app.handlers.save_pre.remove(save_pre_layer_settings)
    bpy.app.handlers.load_post.remove(load_post_purge_settings)
    
    del scene.sm_settings_movieclips, scene.sm_settings_images, scene.sm_bg_type, scene.sm_fg_type
    del scene.sm_background, scene.sm_foreground

    for cls in MODEL_CLASSES:
        bpy.utils.unregister_class(cls)
