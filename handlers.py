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


import bpy
from bpy.app.handlers import persistent

from .layers import copy_settings, set_layer_name


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
        name_list = []
        while index < len(settings_list):
            if settings_list[index].name not in data_list:
                name_list.append(settings_list[index].name)
                settings_list.remove(index)
            else:
                index += 1
        if len(name_list) > 0:
            print('{} layer settings have been removed for the following {}:'.format(len(name_list), print_type))
            for name in name_list:
                print('\t{}'.format(name))

    for scene in bpy.data.scenes:
        purge_layer(scene.sm_settings_movieclips, bpy.data.movieclips, 'movieclips')
        purge_layer(scene.sm_settings_images, bpy.data.images, 'images')


def get_bg_name(self):
    return self.get('sm_bg_name', '')


def get_fg_name(self):
    return self.get('sm_fg_name', '')


def set_bg_name(self, value):
    set_layer_name(self, 'sm_bg_name', self.sm_bg_name, value, self.sm_background, self.sm_bg_type)


def set_fg_name(self, value):
    set_layer_name(self, 'sm_fg_name', self.sm_fg_name, value, self.sm_foreground, self.sm_fg_type)


def bg_update(self, context):
    context.scene.sm_bg_name = ''


def fg_update(self, context):
    context.scene.sm_fg_name = ''
