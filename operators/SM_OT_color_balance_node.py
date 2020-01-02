import bpy
from ..utils import validMaxMinRGB

class SM_OT_color_balance_node(bpy.types.Operator):
    bl_idname = "shot_matcher.color_balance_node"
    bl_label = "Apply Analysis to Compositor"
    bl_description = "Creates a color balance node that maps the max/min values from the foreground to the background layer"
    bl_options = {'REGISTER'}
    
    @classmethod
    def poll(cls, context):
        return context.edit_image is not None
    
    def execute(self, context):
        node_name = "Color Balance: " + context.edit_image.name
        context.scene.use_nodes = True
      
        if validMaxMinRGB(context) is False:
            self.report({'ERROR'}, "The white color is less than or equal to the black color")
            return {'FINISHED'}
        
        tree = bpy.context.scene.node_tree
        cb_node = tree.nodes.get(node_name)
        
        if cb_node is None:    
            #create color balance node
            cb_node = tree.nodes.new(type='CompositorNodeColorBalance', name=node_name)              
            cb_node.correction_method = 'OFFSET_POWER_SLOPE'

        cb_node.offset = context.scene.sm_background.min_color - context.scene.sm_foreground.min_color
        cb_node.slope = (context.scene.sm_background.max_color - context.scene.sm_background.min_color) / (context.scene.sm_foreground.max_color - context.scene.sm_foreground.min_color)
                
        return {'FINISHED'}
