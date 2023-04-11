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

from .ColorPicker import SM_OT_color_picker
from .ResetColorPicker import SM_OT_color_reset
from .AlphaOverNode import SM_OT_alpha_over_node
from .ColorBalanceNode import SM_OT_color_balance_node
from .ImageCalculator import SM_OT_image_calculator
from .SetSelectedLayer import SM_OT_set_selected
from .VideoCalculator import SM_OT_video_calculator
from .VideoFrameCalculator import SM_OT_video_frame_calculator

_register_order = [SM_OT_color_picker, SM_OT_color_reset,
                   SM_OT_alpha_over_node, SM_OT_color_balance_node,
                   SM_OT_image_calculator,
                   SM_OT_set_selected,
                   SM_OT_video_calculator, SM_OT_video_frame_calculator]


def register():
    for cls in _register_order:
        bpy.utils.register_class(cls)


def unregister():
    for cls in _register_order[::-1]:
        bpy.utils.unregister_class(cls)
