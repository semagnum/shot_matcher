import bpy
from ..utils import create_sm_ao_node, validMaxMinRGB, truncate_name

class SM_OT_alpha_over_node(bpy.types.Operator):
    bl_idname = 'shot_matcher.alpha_over_node'
    bl_label = 'Shot Matcher: Alpha Over'
    bl_description = 'Creates an alpha-over node that maps the max/min values from the foreground to the background layer'
    bl_options = {'REGISTER'}
    
    def execute(self, context):
        bg_layer = context.scene.sm_background
        fg_layer = context.scene.sm_foreground
        node_group_name = 'AO: ' + truncate_name(fg_layer.layer_name, 12) + ' -> ' + truncate_name(bg_layer.layer_name, 12)
        context.scene.use_nodes = True
      
        if validMaxMinRGB(context) is False:
            self.report({'ERROR'}, 'The white color is less than or equal to the black color')
            return {'FINISHED'}
        
        try:
            alpha_over_group = create_sm_ao_node(context, node_group_name)
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
            if bg_layer.layer_name != '':
                if bg_layer.layer_type == 'video':
                    bg_node = tree.nodes.new('CompositorNodeMovieClip')
                    bg_node.clip = bpy.data.movieclips[bg_layer.layer_name]
                else:
                    bg_node = tree.nodes.new('CompositorNodeImage')
                    bg_node.image = bpy.data.images[bg_layer.layer_name]
                bg_node.location = -300, 0
                tree.links.new(bg_node.outputs[0], group_node.inputs[0])
            if fg_layer.layer_name != '':
                if fg_layer.layer_type == 'video':
                    fg_node = tree.nodes.new('CompositorNodeMovieClip')
                    fg_node.clip = bpy.data.movieclips[fg_layer.layer_name]
                else:
                    fg_node = tree.nodes.new('CompositorNodeImage')
                    fg_node.image = bpy.data.images[fg_layer.layer_name]
                fg_node.location = -300, -500
                tree.links.new(fg_node.outputs[0], group_node.inputs[1])            
        
        return {'FINISHED'}
