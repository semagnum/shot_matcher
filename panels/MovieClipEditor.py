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

from ..layers import SourceLayer, TargetLayer
from ..operators import SM_OT_alpha_over_node, SM_OT_color_balance_node
from .panel_utils import draw_layer, PANEL_NAME


class SM_PT_video_analyzer_target(bpy.types.Panel):
    bl_space_type = 'CLIP_EDITOR'
    bl_label = 'Target'
    bl_category = PANEL_NAME
    bl_region_type = 'TOOLS'

    def draw(self, context):
        draw_layer(self, context, TargetLayer(context))


class SM_PT_video_analyzer_source(bpy.types.Panel):
    bl_space_type = 'CLIP_EDITOR'
    bl_label = 'Source'
    bl_category = PANEL_NAME
    bl_region_type = 'TOOLS'

    def draw(self, context):
        draw_layer(self, context, SourceLayer(context))


class SM_PT_video_analyzer_apply(bpy.types.Panel):
    bl_space_type = 'CLIP_EDITOR'
    bl_label = 'Apply'
    bl_category = PANEL_NAME
    bl_region_type = 'TOOLS'

    def draw(self, _context):
        layout = self.layout
        layout.operator(SM_OT_color_balance_node.bl_idname, text='Color Balance', icon='COLOR')
        layout.operator(SM_OT_alpha_over_node.bl_idname, text='Alpha Over', icon='RENDERLAYERS')
