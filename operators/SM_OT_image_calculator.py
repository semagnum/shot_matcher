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
from ..utils import get_layer_name
from .op_utils import frame_analyze, get_render_result


class SM_OT_image_calculator(bpy.types.Operator):
    bl_idname = 'shot_matcher.image_calculator'
    bl_label = 'Image Color Analyzer'
    bl_description = 'Calculates the maximum/minimum values for an image'
    bl_options = {'REGISTER'}

    @classmethod
    def poll(cls, context):
        layer = get_layer_name(context)
        return (layer in bpy.data.images) and (bpy.data.images[layer].pixels or bpy.data.images[layer].type == 'RENDER_RESULT')
    
    def execute(self, context):
        context.window.cursor_set('WAIT')
        bpy_image = bpy.data.images[get_layer_name(context)]
        if bpy_image.type == 'RENDER_RESULT':
            image, _, _ = get_render_result(bpy_image)
        else:
            image = bpy_image.pixels
        frame_analyze(context, image)
        
        context.window.cursor_set('DEFAULT')
        return {'FINISHED'}
