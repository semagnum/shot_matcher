import bpy
from ..utils import create_cma_node, validMaxMinRGB

class CMA_OT_add_image_node(bpy.types.Operator):
    bl_idname = "color_matching_analyzer.add_image_node"
    bl_label = "Apply Analysis to Compositor"
    bl_options = {'REGISTER'}
    
    @classmethod
    def poll(cls, context):
        return context.edit_image is not None
    
    def execute(self, context):
        node_group_name = "Alpha Over: " + context.edit_image.name
        context.scene.use_nodes = True
      
        if validMaxMinRGB(context) is False:
            self.report({'ERROR'}, "The white color is less than or equal to the black color")
            return {'FINISHED'}
        
        image_merge_group = create_cma_node(context, node_group_name)
        
        tree = bpy.context.scene.node_tree
        group_node = tree.nodes.get(node_group_name)
        
        if group_node is None:
            group_node = tree.nodes.new("CompositorNodeGroup")
            group_node.node_tree = image_merge_group
            group_node.name = node_group_name
            #add the background texture as an input, just for quicker debugging
            image_node = tree.nodes.new("CompositorNodeImage")
            image_node.image = context.edit_image
            image_node.location = -300, 0
            tree.links.new(image_node.outputs[0], group_node.inputs[0])
        
        #switch views
        context.area.type = 'NODE_EDITOR'
        context.space_data.tree_type = 'CompositorNodeTree'

        
        return {'FINISHED'}