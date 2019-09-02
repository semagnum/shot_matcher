import bpy

def frame_analyze(context, image, forceOverwrite):          
    pixels = image.pixels[:] # create a copy (tuple) for read-only access
    
    #slice the pixels into the RGB channels
    ch_r = pixels[0::4]    
    ch_g = pixels[1::4]
    ch_b = pixels[2::4]
    
    max_r = max(ch_r)
    max_g = max(ch_g)
    max_b = max(ch_b)
    min_r = min(ch_r)
    min_g = min(ch_g)
    min_b = min(ch_b)

    if forceOverwrite is True:
        context.scene.max_color = (max_r, max_g, max_b)
        context.scene.min_color = (min_r, min_g, min_b)
        return True

    #we only want to overwrite if the value supersedes the current one
    maxNewV = RGBtoV(max_r, max_g, max_b)
    maxCurrentV = RGBtoV(context.scene.max_color[0], context.scene.max_color[1], context.scene.max_color[2])

    if maxNewV > maxCurrentV:
        context.scene.max_color = (max_r, max_g, max_b)

    minNewV = RGBtoV(min_r, min_g, min_b)
    minCurrentV = RGBtoV(context.scene.min_color[0], context.scene.min_color[1], context.scene.min_color[2])
    if minNewV < minCurrentV:
        context.scene.min_color = (min_r, min_g, min_b)
    
    return True

def RGBtoV(r, g, b):
    RGBList = [r, g, b]
    return max(RGBList)

def validMaxMinRGB(context):
    minV = RGBtoV(context.scene.min_color[0], context.scene.min_color[1], context.scene.min_color[2])
    maxV = RGBtoV(context.scene.max_color[0], context.scene.max_color[1], context.scene.max_color[2])
  
    return minV <= maxV

def create_cma_node(context, node_group_name):
    # create a group
    image_merge_group = bpy.data.node_groups.get(node_group_name)
    
    if image_merge_group is None:
        image_merge_group = bpy.data.node_groups.new(type="CompositorNodeTree", name=node_group_name)
        # create group inputs
        image_merge_group.inputs.new("NodeSocketColor","Background")
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
    color_node.offset = context.scene.min_color
    color_node.slope = context.scene.max_color - context.scene.min_color
        
    return image_merge_group