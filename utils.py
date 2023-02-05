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


def copy_settings(first_layer, second_layer):
    second_layer.max_color = first_layer.max_color
    second_layer.mid_color = first_layer.mid_color
    second_layer.min_color = first_layer.min_color
    second_layer.use_alpha_threshold = first_layer.use_alpha_threshold
    second_layer.alpha_threshold = first_layer.alpha_threshold
    second_layer.start_frame = first_layer.start_frame
    second_layer.end_frame = first_layer.end_frame
    second_layer.frame_step = first_layer.frame_step


def get_layer_settings(context):
    if context.scene.layer_context == 'bg':
        return context.scene.sm_background
    return context.scene.sm_foreground


def get_layer_name(context):
    if context.scene.layer_context == 'bg':
        return context.scene.sm_bg_name
    return context.scene.sm_fg_name


def get_bg_name(self):
    return self.get('sm_bg_name', '')


def get_fg_name(self):
    return self.get('sm_fg_name', '')


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


def set_bg_name(self, value):
    set_layer_name(self, 'sm_bg_name', self.sm_bg_name, value, self.sm_background, self.sm_bg_type)


def set_fg_name(self, value):
    set_layer_name(self, 'sm_fg_name', self.sm_fg_name, value, self.sm_foreground, self.sm_fg_type)


def type_update(self, context):
    if context.scene.layer_context == 'bg':
        context.scene.sm_bg_name = ''
    else:
        context.scene.sm_fg_name = ''
