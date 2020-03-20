import bpy
from ..utils import validMaxMinRGB, truncate_name, colorDivision

class SM_OT_alpha_over_node(bpy.types.Operator):
    bl_idname = 'shot_matcher.alpha_over_node'
    bl_label = 'Shot Matcher: Alpha Over'
    bl_description = 'Creates an alpha-over node that maps the max/min values from the foreground to the background layer'
    bl_options = {'REGISTER'}

    def create_sm_ao_node(self, context, node_group_name):
        # create a group
        image_merge_group = bpy.data.node_groups.get(node_group_name)
        
        if image_merge_group is None:
            image_merge_group = bpy.data.node_groups.new(type='CompositorNodeTree', name=node_group_name)
            # create group inputs
            image_merge_group.inputs.new('NodeSocketColor','Background')
            image_merge_group.inputs.new('NodeSocketColor','Foreground')
            group_inputs = image_merge_group.nodes.new('NodeGroupInput')
            group_inputs.location = (-250,0)
            # create group outputs
            image_merge_group.outputs.new('NodeSocketColor','Image')
            group_outputs = image_merge_group.nodes.new('NodeGroupOutput')
            group_outputs.location = (900,0)        
            #create color balance node
            color_node = image_merge_group.nodes.new(type='CompositorNodeColorBalance')              
            color_node.correction_method = 'OFFSET_POWER_SLOPE'      
            #create alpha over node      
            alpha_over_node = image_merge_group.nodes.new(type='CompositorNodeAlphaOver')
            alpha_over_node.location = 600, 200
            alpha_over_node.use_premultiply = True               
            #bring it all together
            image_merge_group.links.new(color_node.outputs[0], alpha_over_node.inputs[2])
            image_merge_group.links.new(group_inputs.outputs['Background'], alpha_over_node.inputs[1])
            image_merge_group.links.new(group_inputs.outputs['Foreground'], color_node.inputs[1])
            image_merge_group.links.new(alpha_over_node.outputs[0], group_outputs.inputs['Image'])

        color_node = image_merge_group.nodes.get('Color Balance')
        bg_layer = context.scene.sm_background
        fg_layer = context.scene.sm_foreground
        bg_slope = bg_layer.max_color - bg_layer.min_color
        fg_slope = fg_layer.max_color - fg_layer.min_color
        try:
            color_node.slope = colorDivision(bg_slope, fg_slope)
        except:
            raise ZeroDivisionError('Failed: division by zero ([foreground white color] - [foreground black color] must not equal zero!)')
        color_node.offset = bg_layer.min_color - fg_layer.min_color
            
        return image_merge_group
    
    def execute(self, context):
        bg_layer = context.scene.sm_background
        fg_layer = context.scene.sm_foreground
        bg_name = context.scene.sm_bg_name
        fg_name = context.scene.sm_fg_name
        node_group_name = 'AO: ' + truncate_name(fg_name, 12) + ' -> ' + truncate_name(bg_name, 12)
        context.scene.use_nodes = True
      
        if validMaxMinRGB(context) is False:
            self.report({'ERROR'}, 'The white color is less than or equal to the black color')
            return {'FINISHED'}
        
        try:
            alpha_over_group = self.create_sm_ao_node(context, node_group_name)
        except ZeroDivisionError as err:
            self.report({'ERROR'}, err)
            return {'FINISHED'}
        
        tree = bpy.context.scene.node_tree
        group_node = tree.nodes.get(node_group_name)
        
        if group_node is None:
            group_node = tree.nodes.new('CompositorNodeGroup')
            group_node.node_tree = alpha_over_group
            group_node.name = node_group_name
            #add the background texture as an input, just for quicker debugging
            if bg_name != '':
                if bg_layer.layer_type == 'video':
                    bg_node = tree.nodes.new('CompositorNodeMovieClip')
                    bg_node.clip = bpy.data.movieclips[bg_name]
                else:
                    bg_node = tree.nodes.new('CompositorNodeImage')
                    bg_node.image = bpy.data.images[bg_name]
                bg_node.location = -300, 0
                tree.links.new(bg_node.outputs[0], group_node.inputs[0])
            if fg_name != '':
                if fg_layer.layer_type == 'video':
                    fg_node = tree.nodes.new('CompositorNodeMovieClip')
                    fg_node.clip = bpy.data.movieclips[fg_name]
                else:
                    fg_node = tree.nodes.new('CompositorNodeImage')
                    fg_node.image = bpy.data.images[fg_name]
                fg_node.location = -300, -500
                tree.links.new(fg_node.outputs[0], group_node.inputs[1])            
        
        return {'FINISHED'}
