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

from .op_utils import valid_rgb_range, truncate_name, offset_power_slope


class SM_OT_color_balance_node(bpy.types.Operator):
    bl_idname = 'shot_matcher.color_balance_node'
    bl_label = 'Shot Matcher to Color Balance'
    bl_description = 'Creates a color balance node that maps max/min values from the foreground to the background layer'
    bl_options = {'REGISTER', 'UNDO'}

    use_midtones: bpy.props.BoolProperty(name="Use midtones",
                                         description="Compute color balance power using midtones,"
                                                     "otherwise set it to default value")

    def execute(self, context):
        node_name = 'CB: ' + truncate_name(context.scene.sm_fg_name, 12) + ' -> ' + truncate_name(
            context.scene.sm_bg_name, 12)
        context.scene.use_nodes = True

        if valid_rgb_range(context) is False:
            self.report({'ERROR'}, 'The white color is less than or equal to the black color')
            return {'FINISHED'}

        tree = context.scene.node_tree
        cb_node = next((node for node in tree.nodes if node.label == node_name), None)

        if cb_node is None:
            # create color balance node
            cb_node = tree.nodes.new(type='CompositorNodeColorBalance')
            cb_node.correction_method = 'OFFSET_POWER_SLOPE'
            cb_node.label = node_name

        try:
            basis, offset, power, slope = offset_power_slope(context)
            cb_node.slope = slope
            cb_node.offset = offset
            cb_node.power = power if self.use_midtones else (1.0, 1.0, 1.0)
            cb_node.offset_basis = basis
        except ZeroDivisionError:
            self.report({'ERROR'}, 'Failed: division by zero ([white color] - [black color] must not equal zero!)')
            return {'FINISHED'}

        return {'FINISHED'}
