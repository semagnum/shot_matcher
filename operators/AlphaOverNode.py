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
from .op_utils import truncate_name, valid_rgb_range, offset_power_slope


def create_layer_node(context, tree, layer_name, layer_type):
    if layer_type == 'video':
        layer_node = tree.nodes.new('CompositorNodeMovieClip')
        layer_node.clip = bpy.data.movieclips[layer_name]
        return layer_node

    # is an image
    bpy_img = bpy.data.images[layer_name]
    if bpy_img.type == 'RENDER_RESULT':
        layer_node = tree.nodes.new('CompositorNodeRLayers')
        layer_node.scene = context.scene
    else:
        layer_node = tree.nodes.new('CompositorNodeImage')
        layer_node.image = bpy.data.images[layer_name]
    return layer_node


def create_sm_ao_node(context, node_group_name, use_midtones):
    # create a group
    image_merge_group = bpy.data.node_groups.get(node_group_name)

    if image_merge_group is None:
        image_merge_group = bpy.data.node_groups.new(type='CompositorNodeTree', name=node_group_name)
        # create group inputs
        image_merge_group.inputs.new('NodeSocketColor', 'Background')
        image_merge_group.inputs.new('NodeSocketColor', 'Foreground')
        group_inputs = image_merge_group.nodes.new('NodeGroupInput')
        group_inputs.location = (-250, 0)
        # create group outputs
        image_merge_group.outputs.new('NodeSocketColor', 'Image')
        group_outputs = image_merge_group.nodes.new('NodeGroupOutput')
        group_outputs.location = (900, 0)
        # create color balance node
        color_node = image_merge_group.nodes.new(type='CompositorNodeColorBalance')
        color_node.correction_method = 'OFFSET_POWER_SLOPE'
        # create alpha over node
        alpha_over_node = image_merge_group.nodes.new(type='CompositorNodeAlphaOver')
        alpha_over_node.location = 600, 200
        alpha_over_node.use_premultiply = True
        # bring it all together
        image_merge_group.links.new(color_node.outputs[0], alpha_over_node.inputs[2])
        image_merge_group.links.new(group_inputs.outputs['Background'], alpha_over_node.inputs[1])
        image_merge_group.links.new(group_inputs.outputs['Foreground'], color_node.inputs[1])
        image_merge_group.links.new(alpha_over_node.outputs[0], group_outputs.inputs['Image'])

    color_node = image_merge_group.nodes.get('Color Balance')
    try:
        basis, offset, power, slope = offset_power_slope(context)
        color_node.slope = slope
        color_node.offset = offset
        color_node.power = power if use_midtones else (1.0, 1.0, 1.0)
        color_node.offset_basis = basis
    except ZeroDivisionError:
        raise ZeroDivisionError('Failed: division by zero ([white color] - [black color] must not equal zero!)')

    return image_merge_group


class SM_OT_alpha_over_node(bpy.types.Operator):
    bl_idname = 'shot_matcher.alpha_over_node'
    bl_label = 'Shot Matcher to Alpha Over'
    bl_description = 'Creates an alpha-over node that maps max/min values from the foreground to the background layer'
    bl_options = {'REGISTER', 'UNDO'}

    use_midtones: bpy.props.BoolProperty(name="Use midtones",
                                        description="Compute color balance power using midtones,"
                                                    "otherwise set it to default value")

    def execute(self, context):
        bg_name = context.scene.sm_bg_name
        fg_name = context.scene.sm_fg_name
        node_group_name = 'AO: ' + truncate_name(fg_name, 12) + ' -> ' + truncate_name(bg_name, 12)
        context.scene.use_nodes = True

        if valid_rgb_range(context) is False:
            self.report({'ERROR'}, 'The white color is less than or equal to the black color')
            return {'FINISHED'}

        try:
            alpha_over_group = create_sm_ao_node(context, node_group_name, self.use_midtones)
        except ZeroDivisionError as err:
            self.report({'ERROR'}, err)
            return {'FINISHED'}

        tree = bpy.context.scene.node_tree
        group_node = tree.nodes.get(node_group_name)

        if group_node is None:
            group_node = tree.nodes.new('CompositorNodeGroup')
            group_node.node_tree = alpha_over_group
            group_node.name = node_group_name
            # add the background texture as an input, just for quicker debugging
            if bg_name != '':
                bg_node = create_layer_node(context, tree, bg_name, context.scene.sm_bg_type)
                bg_node.location = -300, 0
                tree.links.new(bg_node.outputs[0], group_node.inputs[0])
            if fg_name != '':
                fg_node = create_layer_node(context, tree, fg_name, context.scene.sm_fg_type)
                fg_node.location = -300, -500
                tree.links.new(fg_node.outputs[0], group_node.inputs[1])

        return {'FINISHED'}
