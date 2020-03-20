import bpy
import numpy as np

def copy_settings(first_layer, second_layer):
    second_layer.max_color = first_layer.max_color
    second_layer.min_color = first_layer.min_color
    second_layer.use_alpha_threshold = first_layer.use_alpha_threshold
    second_layer.alpha_threshold = first_layer.alpha_threshold
    second_layer.start_frame = first_layer.start_frame
    second_layer.end_frame = first_layer.end_frame
    second_layer.frame_step = first_layer.frame_step

def get_layer_settings(context):
    if context.scene.layer_context == 'bg':
        return context.scene.sm_background
    return context.scene.sm_foreground

def get_layer_name(context):
    if context.scene.layer_context == 'bg':
        return context.scene.sm_bg_name
    return context.scene.sm_fg_name

def get_bg_name(self):
    return self.get('sm_bg_name', '')

def get_fg_name(self):
    return self.get('sm_fg_name', '')

def set_layer_name(itself, layer_name, old_value, new_value, sm_layer, sm_layer_type):
    if new_value == '':
        itself[layer_name] = new_value
        return
    
    if sm_layer_type == 'video':
        layer_dict = itself.sm_settings_movieclips
    else:
        layer_dict = itself.sm_settings_images
    
    current_index = layer_dict.find(old_value)
    if old_value != '':
        if current_index == -1:
            current_layer = layer_dict.add()
            current_layer.name = old_value
            copy_settings(sm_layer, current_layer.setting)
        else:
            copy_settings(sm_layer, layer_dict[current_index].setting)
   
    new_index = layer_dict.find(new_value)
    if new_index == -1:
        new_layer = layer_dict.add()
        new_layer.name = new_value
        copy_settings(new_layer.setting, sm_layer)
    else:
        copy_settings(layer_dict[new_index].setting, sm_layer)

    itself[layer_name] = new_value

def set_bg_name(self, value):
    set_layer_name(self, 'sm_bg_name', self.sm_bg_name, value, self.sm_background, self.sm_bg_type)

def set_fg_name(self, value):
    set_layer_name(self, 'sm_fg_name', self.sm_fg_name, value, self.sm_foreground, self.sm_fg_type)

def type_update(self, context):
    layer_name = get_layer_name(context)
    layer_name = ''

def truncate_name(name, limit):
    return (name[:(limit - 3)] + '...') if len(name) > limit else name

def frame_analyze(context, image, forceOverwrite):  
    layer = get_layer_settings(context)        
    pixels = np.array(image.pixels)
    
    #slice the pixels into the RGB channels
    ch_r = pixels[0::4]    
    ch_g = pixels[1::4]
    ch_b = pixels[2::4]
    if layer.use_alpha_threshold:
        ch_a = pixels[3::4]
        ch_r = ch_r[(ch_a >= layer.alpha_threshold)]
        ch_g = ch_g[(ch_a >= layer.alpha_threshold)]
        ch_b = ch_b[(ch_a >= layer.alpha_threshold)]
    
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
    maxNewV = max(max_r, max_g, max_b)
    maxCurrentV = max(layer.max_color)

    if maxNewV > maxCurrentV:
        layer.max_color = (max_r, max_g, max_b)

    minNewV = max(min_r, min_g, min_b)
    minCurrentV = max(layer.min_color)
    if minNewV < minCurrentV:
        layer.min_color = (min_r, min_g, min_b)
    
    return True

def validMaxMinRGB(context):
    def validLayerMaxMin(context, layer):
        minV = max(layer.min_color)
        maxV = max(layer.max_color)
        return minV <= maxV
    
    return validLayerMaxMin(context, context.scene.sm_background) and validLayerMaxMin(context, context.scene.sm_foreground)

def colorDivision(color1, color2):
   return (color1[0] / color2[0], color1[1] / color2[1], color1[2] / color2[2])
