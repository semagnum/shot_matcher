import bpy
from ..utils import validMaxMinRGB

class SM_OT_color_balance_node(bpy.types.Operator):
    bl_idname = 'shot_matcher.color_balance_node'
    bl_label = 'Shot Matcher: Color Balance'
    bl_description = 'Creates a color balance node that maps the max/min values from the foreground to the background layer'
    bl_options = {'REGISTER'}
    
    @classmethod
    def poll(cls, context):
        return (context.scene.sm_background.layer_name is not None) and (context.scene.sm_foreground.layer_name is not None)
    
    def execute(self, context):
        bg_layer = context.scene.sm_background
        fg_layer = context.scene.sm_foreground
        node_name = 'Color Balance: ' + fg_layer.layer_name + ' -> ' + bg_layer.layer_name
        context.scene.use_nodes = True
      
        if validMaxMinRGB(context) is False:
            self.report({'ERROR'}, 'The white color is less than or equal to the black color')
            return {'FINISHED'}
        
        tree = bpy.context.scene.node_tree
        cb_node = tree.nodes.get(node_name)
        
        if cb_node is None:    
            #create color balance node
            cb_node = tree.nodes.new(type='CompositorNodeColorBalance', name=node_name)              
            cb_node.correction_method = 'OFFSET_POWER_SLOPE'

        cb_node.offset = bg_layer.min_color - fg_layer.min_color
        cb_node.slope = (bg_layer.max_color - bg_layer.min_color) / (fg_layer.max_color - fg_layer.min_color)
                
        return {'FINISHED'}
