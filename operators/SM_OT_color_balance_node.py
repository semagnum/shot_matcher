import bpy

from .op_utils import valid_rgb_range, truncate_name, offset_power_slope


class SM_OT_color_balance_node(bpy.types.Operator):
    bl_idname = 'shot_matcher.color_balance_node'
    bl_label = 'Shot Matcher: Color Balance'
    bl_description = 'Creates a color balance node that maps max/min values from the foreground to the background layer'
    bl_options = {'REGISTER'}

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
            cb_node.power = power
            cb_node.offset_basis = basis
        except ZeroDivisionError:
            self.report({'ERROR'}, 'Failed: division by zero ([white color] - [black color] must not equal zero!)')
            return {'FINISHED'}

        return {'FINISHED'}
