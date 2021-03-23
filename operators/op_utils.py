from math import floor
import numpy as np
from ..utils import get_layer_settings

def truncate_name(name, limit):
    return (name[:(limit - 3)] + '...') if len(name) > limit else name

# returns the midtone color for use by the video analyzer
def frame_analyze(context, image):  
    layer = get_layer_settings(context)        
    pixels = np.array(image).reshape(-1, 4)
    
    #slice the pixels into the RGB channels
    if layer.use_alpha_threshold:
        ch_a = pixels[:, 3]
        pixels = pixels[(ch_a >= layer.alpha_threshold)]
    
    pixels = np.delete(pixels, 3, axis=1)
    img_max = pixels.max(axis=0)
    img_min = pixels.min(axis=0)
    img_mid = pixels.mean(axis=0)

    layer.max_color = tuple(img_max)
    layer.mid_color = tuple(img_mid)
    layer.min_color = tuple(img_min)

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
