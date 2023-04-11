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
from .op_utils import frame_analyze, get_render_result, valid_image


class SM_OT_image_calculator(bpy.types.Operator):
    bl_idname = 'shot_matcher.image_calculator'
    bl_label = 'Image Color Analyzer'
    bl_description = 'Calculates the maximum/minimum values for an image'
    bl_options = {'REGISTER'}

    layer_type: bpy.props.StringProperty()
    
    def execute(self, context):
        layer = build_layer_type(context, self.layer_type)
        layer_name = layer.name

        images = bpy.data.images
        if layer_name not in bpy.data.images or not valid_image(images[layer_name]):
            self.report({'ERROR'}, 'Must have a valid image selected')
            return {'CANCELLED'}

        bpy_image = bpy.data.images[layer_name]

        context.window.cursor_set('WAIT')
        if bpy_image.type == 'RENDER_RESULT':
            image, _, _ = get_render_result(bpy_image)
        else:
            image = bpy_image.pixels
        frame_analyze(image, layer.settings)
        
        context.window.cursor_set('DEFAULT')
        return {'FINISHED'}
