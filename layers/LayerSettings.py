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


class LayerSettings(bpy.types.PropertyGroup):
    max_color: bpy.props.FloatVectorProperty(
        description='The color representing the white value of this layer',
        default=(1.0, 1.0, 1.0),
        min=0.0,
        precision=4,
        subtype='COLOR')

    mid_color: bpy.props.FloatVectorProperty(
        description='The color representing the midtone value of this layer',
        default=(0.5, 0.5, 0.5),
        min=0.0,
        precision=4,
        subtype='COLOR')

    min_color: bpy.props.FloatVectorProperty(
        description='The color representing the black value of this layer',
        default=(0.0, 0.0, 0.0),
        min=0.0,
        precision=4,
        subtype='COLOR')

    use_alpha_threshold: bpy.props.BoolProperty(default=False, name='Use Alpha Threshold')
    alpha_threshold: bpy.props.FloatProperty(name='Alpha Threshold',
                                             description='Threshold of a pixel\'s alpha value to be used for analysis',
                                             default=0.75, min=0.0, max=1.0,
                                             step=5, precision=2)

    start_frame: bpy.props.IntProperty(default=1)
    end_frame: bpy.props.IntProperty(default=250)
    frame_step: bpy.props.IntProperty(
        default=10,
        min=1)
