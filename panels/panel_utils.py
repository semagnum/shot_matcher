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

from ..operators import SM_OT_color_picker, SM_OT_color_reset, SM_OT_set_selected
from ..operators import SM_OT_image_calculator, SM_OT_video_calculator, SM_OT_video_frame_calculator

from ..layers import BaseLayer


PANEL_NAME = 'Shot Matcher'


def draw_layer(itself, context, layer: BaseLayer):
    layout = itself.layout

    layer_props = layer.settings
    media_type = layer.media_type
    layer_name = layer.name_str

    layer_type = layer.layer_type

    box = layout.box()
    box.row().prop(context.scene, layer.media_type_str, expand=True)

    if media_type == 'video':
        box.prop_search(context.scene, layer_name, bpy.data, 'movieclips', text='File',
                        icon='FILE_MOVIE')
        if itself.bl_space_type == 'CLIP_EDITOR':
            op = box.operator(SM_OT_set_selected.bl_idname, text='Use Current Clip',
                         icon='WINDOW')
            op.space_type = 'CLIP_EDITOR'
            op.layer_type = layer_type
    else:
        box.prop_search(context.scene, layer_name, bpy.data, 'images', text='File',
                        icon='FILE_IMAGE')
        if itself.bl_space_type == 'IMAGE_EDITOR':
            op = box.operator(SM_OT_set_selected.bl_idname, text='Use Current Image',
                         icon='WINDOW')
            op.space_type = 'IMAGE_EDITOR'
            op.layer_type = layer_type

    box.prop(layer_props, 'use_alpha_threshold')
    if layer_props.use_alpha_threshold:
        box.prop(layer_props, 'alpha_threshold', slider=True)

    box.row().prop(layer_props, 'max_color', text='White')
    box.row().prop(layer_props, 'mid_color', text='Midtone')
    box.row().prop(layer_props, 'min_color', text='Black')

    if media_type == 'video' and itself.bl_space_type == 'CLIP_EDITOR':
        op = box.operator(SM_OT_video_frame_calculator.bl_idname, text='Analyze Video Frame', icon='SEQ_HISTOGRAM')
        op.layer_type = layer_type

    col = box.column(align=True)
    if media_type == 'image':
        if itself.bl_space_type == 'IMAGE_EDITOR':
            op = col.operator(SM_OT_color_picker.bl_idname, text='Color Pick White and Black', icon='EYEDROPPER')
            op.layer_type = layer_type

            op = col.operator(SM_OT_color_reset.bl_idname, text='Reset Color Picker', icon='IMAGE_ALPHA')
            op.layer_type = layer_type

        op = box.operator(SM_OT_image_calculator.bl_idname, text='Analyze Image', icon='SEQ_HISTOGRAM')
        op.layer_type = layer_type
    else:
        col.prop(layer_props, 'start_frame', text='Start Frame')
        col.prop(layer_props, 'end_frame', text='End Frame')
        col.prop(layer_props, 'frame_step', text='Frame Step')

        op = col.operator(SM_OT_video_calculator.bl_idname, text='Analyze Video Range', icon='SEQ_HISTOGRAM')
        op.layer_type = layer_type
