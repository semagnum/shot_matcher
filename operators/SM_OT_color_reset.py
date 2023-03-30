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

from ..layers import build_layer_type


class SM_OT_color_reset(bpy.types.Operator):
    bl_idname = 'shot_matcher.color_reset'
    bl_label = 'Reset Min and Max Colors'
    bl_description = 'Resets the maximum and minimum color values for use with the color picker'
    bl_options = {'REGISTER', 'UNDO'}

    layer_type: bpy.props.StringProperty()
    
    def execute(self, context):
        settings = build_layer_type(context, self.layer_type).settings
        max_color = (10000.0, 10000.0, 10000.0)
        min_color = (0.0, 0.0, 0.0)
        settings.max_color = min_color
        settings.min_color = max_color
        return {'FINISHED'}
