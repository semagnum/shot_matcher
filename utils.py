import bpy
import numpy as np

def get_layer_settings(context):
    if context.scene.layer_context == 'bg':
        return context.scene.sm_background
    return context.scene.sm_foreground

def frame_analyze(context, image, forceOverwrite):  
    layer = get_layer_settings(context)        
    pixels = np.array(image.pixels)
    
    #slice the pixels into the RGB channels
    ch_r = pixels[0::4]    
    ch_g = pixels[1::4]
    ch_b = pixels[2::4]
    if layer.sm_use_alpha_threshold:
        ch_a = pixels[3::4]
        ch_r = ch_r[(ch_a >= layer.sm_alpha_threshold)]
        ch_g = ch_g[(ch_a >= layer.sm_alpha_threshold)]
        ch_b = ch_b[(ch_a >= layer.sm_alpha_threshold)]
    
    max_r = ch_r.max()
    max_g = ch_g.max()
    max_b = ch_b.max()
    min_r = ch_r.min()
    min_g = ch_g.min()
    min_b = ch_b.min()

    if forceOverwrite is True:
        layer.max_color = (max_r, max_g, max_b)
        layer.min_color = (min_r, min_g, min_b)
        return True

    #we only want to overwrite if the value supersedes the current one
    maxNewV = RGBtoV(max_r, max_g, max_b)
    maxCurrentV = RGBtoV(layer.max_color[0], layer.max_color[1], layer.max_color[2])

    if maxNewV > maxCurrentV:
        layer.max_color = (max_r, max_g, max_b)

    minNewV = RGBtoV(min_r, min_g, min_b)
    minCurrentV = RGBtoV(layer.min_color[0], layer.min_color[1], layer.min_color[2])
    if minNewV < minCurrentV:
        layer.min_color = (min_r, min_g, min_b)
    
    return True

def RGBtoV(r, g, b):
    return max([r, g, b])

def validMaxMinRGB(context):

    def validLayerMaxMin(context, layer):
        minV = RGBtoV(layer.min_color[0], layer.min_color[1], layer.min_color[2])
        maxV = RGBtoV(layer.max_color[0], layer.max_color[1], layer.max_color[2])
        return minV <= maxV
    
    return validLayerMaxMin(context, context.scene.sm_background) and validLayerMaxMin(context, context.scene.sm_foreground)

def create_sm_ao_node(context, node_group_name):
    # create a group
    image_merge_group = bpy.data.node_groups.get(node_group_name)
    
    if image_merge_group is None:
        image_merge_group = bpy.data.node_groups.new(type="CompositorNodeTree", name=node_group_name)
        # create group inputs
        image_merge_group.inputs.new('NodeSocketColor',"Background")
        image_merge_group.inputs.new("NodeSocketColor","Foreground")
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
        alpha_over_node = image_merge_group.nodes.new(type="CompositorNodeAlphaOver")
        alpha_over_node.location = 600, 200
        alpha_over_node.use_premultiply = True               
        #bring it all together
        image_merge_group.links.new(color_node.outputs[0], alpha_over_node.inputs[2])
        image_merge_group.links.new(group_inputs.outputs["Background"], alpha_over_node.inputs[1])
        image_merge_group.links.new(group_inputs.outputs["Foreground"], color_node.inputs[1])
        image_merge_group.links.new(alpha_over_node.outputs[0], group_outputs.inputs['Image'])

    color_node = image_merge_group.nodes.get("Color Balance")
    color_node.offset = context.scene.sm_background.min_color - context.scene.sm_foreground.min_color
    color_node.slope = (context.scene.sm_background.max_color - context.scene.sm_background.min_color) / (context.scene.sm_foreground.max_color - context.scene.sm_foreground.min_color)
        
    return image_merge_group
