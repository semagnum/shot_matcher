"""
Copyright (C) 2023 Spencer Magnusson
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
    reloadable_modules = [
        'layer_base',
        'layer_source',
        'layer_target',
        'layer_props',
        'layer_dict',
    ]
    for module_name in reloadable_modules:
        if module_name in locals():
            importlib.reload(locals()[module_name])

from . import layer_base, layer_source, layer_target, layer_dict, layer_props


from .layer_base import BaseLayer
from .layer_source import SourceLayer
from .layer_target import TargetLayer

from .layer_dict import LayerDict
from .layer_props import LayerSettings

LAYER_TYPES = {
    'target': TargetLayer,
    'source': SourceLayer
}


def build_layer_type(context, layer_type: str):
    return LAYER_TYPES.get(layer_type, BaseLayer)(context)


def copy_settings(first_layer_prop, second_layer_prop):
    second_layer_prop.max_color = first_layer_prop.max_color
    second_layer_prop.mid_color = first_layer_prop.mid_color
    second_layer_prop.min_color = first_layer_prop.min_color
    second_layer_prop.use_alpha_threshold = first_layer_prop.use_alpha_threshold
    second_layer_prop.alpha_threshold = first_layer_prop.alpha_threshold
    second_layer_prop.start_frame = first_layer_prop.start_frame
    second_layer_prop.end_frame = first_layer_prop.end_frame
    second_layer_prop.frame_step = first_layer_prop.frame_step


def set_layer_name(itself, layer_name, old_value, new_value, sm_layer, sm_layer_type):
    if new_value == '':
        itself[layer_name] = new_value
        return

    if sm_layer_type == 'video':
        layer_dict = itself.sm_settings_movieclips
    else:
        layer_dict = itself.sm_settings_images

    current_index = layer_dict.find(old_value)
    if old_value != '':
        if current_index == -1:
            current_layer = layer_dict.add()
            current_layer.name = old_value
            copy_settings(sm_layer, current_layer.setting)
        else:
            copy_settings(sm_layer, layer_dict[current_index].setting)

    new_index = layer_dict.find(new_value)
    if new_index == -1:
        new_layer = layer_dict.add()
        new_layer.name = new_value
        copy_settings(new_layer.setting, sm_layer)
    else:
        copy_settings(layer_dict[new_index].setting, sm_layer)

    itself[layer_name] = new_value
