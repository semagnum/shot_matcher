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

from ..operators.SM_OT_color_balance_node import SM_OT_color_balance_node
from ..operators.SM_OT_alpha_over_node import SM_OT_alpha_over_node
from ..operators.SM_OT_color_picker import SM_OT_color_picker
from ..operators.SM_OT_color_reset import SM_OT_color_reset
from ..operators.SM_OT_image_calculator import SM_OT_image_calculator
from ..operators.SM_OT_video_calculator import SM_OT_video_calculator
from ..operators.SM_OT_set_selected import SM_OT_set_selected
from ..operators.SM_OT_video_frame_calculator import SM_OT_video_frame_calculator

from ..utils import get_layer_settings


def get_layer_type(context):
    if context.scene.layer_context == 'bg':
        return context.scene.sm_bg_type
    return context.scene.sm_fg_type


def get_layer_type_string(context):
    if context.scene.layer_context == 'bg':
        return 'sm_bg_type'
    return 'sm_fg_type'


def get_layer_name_string(context):
    if context.scene.layer_context == 'bg':
        return 'sm_bg_name'
    return 'sm_fg_name'


def draw_layer(itself, context, sm_layer, sm_layer_type):
    layout = itself.layout

    box = layout.box()
    box.row().prop(context.scene, get_layer_type_string(context), expand=True)

    if sm_layer_type == 'video':
        box.prop_search(context.scene, get_layer_name_string(context), bpy.data, 'movieclips', text='File',
                        icon='FILE_MOVIE')
        if itself.bl_space_type == 'CLIP_EDITOR':
            box.operator(SM_OT_set_selected.bl_idname, text='Use Current Clip',
                         icon='WINDOW').space_type = 'CLIP_EDITOR'
    else:
        box.prop_search(context.scene, get_layer_name_string(context), bpy.data, 'images', text='File',
                        icon='FILE_IMAGE')
        if itself.bl_space_type == 'IMAGE_EDITOR':
            box.operator(SM_OT_set_selected.bl_idname, text='Use Current Image',
                         icon='WINDOW').space_type = 'IMAGE_EDITOR'

    box.prop(sm_layer, 'use_alpha_threshold')
    if sm_layer.use_alpha_threshold:
        box.prop(sm_layer, 'alpha_threshold', slider=True)

    box.row().prop(sm_layer, 'max_color', text='White')
    box.row().prop(sm_layer, 'mid_color', text='Midtone')
    box.row().prop(sm_layer, 'min_color', text='Black')

    if sm_layer_type == 'video' and itself.bl_space_type == 'CLIP_EDITOR':
        box.operator(SM_OT_video_frame_calculator.bl_idname, text='Analyze Video Frame', icon='SEQ_HISTOGRAM')

    col = box.column(align=True)
    if sm_layer_type == 'image':
        if itself.bl_space_type == 'IMAGE_EDITOR':
            col.operator(SM_OT_color_picker.bl_idname, text='Color Pick White and Black', icon='EYEDROPPER')
            col.operator(SM_OT_color_reset.bl_idname, text='Reset Color Picker', icon='IMAGE_ALPHA')
        box.operator(SM_OT_image_calculator.bl_idname, text='Analyze Image', icon='SEQ_HISTOGRAM')
    else:
        col.prop(sm_layer, 'start_frame', text='Start Frame')
        col.prop(sm_layer, 'end_frame', text='End Frame')
        col.prop(sm_layer, 'frame_step', text='Frame Step')
        col.operator(SM_OT_video_calculator.bl_idname, text='Analyze Video Range', icon='SEQ_HISTOGRAM')


def draw_panel(itself, context):
    layout = itself.layout

    layout.prop(context.scene, 'layer_context', expand=True)

    draw_layer(itself, context, get_layer_settings(context), get_layer_type(context))

    layout.label(text='Apply to Node Group:')

    layout.operator(SM_OT_color_balance_node.bl_idname, text='Color Balance', icon='COLOR')
    layout.operator(SM_OT_alpha_over_node.bl_idname, text='Alpha Over', icon='RENDERLAYERS')
