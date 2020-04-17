from math import floor
import numpy as np
from ..utils import get_layer_settings

def truncate_name(name, limit):
    return (name[:(limit - 3)] + '...') if len(name) > limit else name

# returns the midtone color for use by the video analyzer
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

    mid_r = np.mean(ch_r)
    mid_g = np.mean(ch_g)
    mid_b = np.mean(ch_b)

    if forceOverwrite is True:
        layer.max_color = (max_r, max_g, max_b)
        layer.mid_color = (mid_r, mid_g, mid_b)
        layer.min_color = (min_r, min_g, min_b)
        return layer.mid_color

    #we only want to overwrite if the value supersedes the current one
    maxNewV = max(max_r, max_g, max_b)
    maxCurrentV = max(layer.max_color)

    if maxNewV > maxCurrentV:
        layer.max_color = (max_r, max_g, max_b)

    minNewV = max(min_r, min_g, min_b)
    minCurrentV = max(layer.min_color)
    if minNewV < minCurrentV:
        layer.min_color = (min_r, min_g, min_b)
    
    return layer.mid_color

def validMaxMinRGB(context):
    def validLayerMaxMin(context, layer):
        minV = max(layer.min_color)
        maxV = max(layer.max_color)
        return minV <= maxV
    
    return validLayerMaxMin(context, context.scene.sm_background) and validLayerMaxMin(context, context.scene.sm_foreground)

def colorDivision(color1, color2):
    return tuple([i / j for i,j in zip(color1, color2)])

def offset_power_slope(context):
    bg_layer = context.scene.sm_background
    fg_layer = context.scene.sm_foreground

    bg_slope = bg_layer.max_color - bg_layer.min_color
    fg_slope = fg_layer.max_color - fg_layer.min_color
    slope = colorDivision(bg_slope, fg_slope)

    bg_power = colorDivision(tuple(ti/2 for ti in bg_slope), bg_layer.mid_color)
    fg_power = colorDivision(tuple(ti/2 for ti in fg_slope), fg_layer.mid_color)
    power = colorDivision(bg_power, fg_power)

    offset = bg_layer.min_color - fg_layer.min_color
    basis = min(offset)
    offset = tuple([val - basis for val in list(offset)])

    return basis, offset, power, slope