"""
Copyright (C) 2023 Spencer Magnusson
semagnum@gmail.com
Created by Spencer Magnusson
    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.
    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.
    You should have received a copy of the GNU General Public License
    along with this program.  If not, see <http://www.gnu.org/licenses/>.
"""


import gpu
import numpy as np


def valid_image(image):
    return image is not None and (image.pixels or image.type == 'RENDER_RESULT')


def truncate_name(name, limit):
    return (name[:(limit - 3)] + '...') if len(name) > limit else name


# returns the midtone color for use by the video analyzer
def frame_analyze(image, layer_settings):
    pixels = np.array(image).reshape(-1, 4)

    # slice the pixels into the RGB channels
    if layer_settings.use_alpha_threshold:
        ch_a = pixels[:, 3]
        pixels = pixels[(ch_a >= layer_settings.alpha_threshold)]

    pixels = np.delete(pixels, 3, axis=1)
    img_max = pixels.max(axis=0)
    img_min = pixels.min(axis=0)
    img_mid = pixels.mean(axis=0)

    layer_settings.max_color = tuple(img_max)
    layer_settings.mid_color = tuple(img_mid)
    layer_settings.min_color = tuple(img_min)


def valid_rgb_range(context):
    def valid_layer_max_min(layer):
        min_v = max(layer.min_color)
        max_v = max(layer.max_color)
        return min_v <= max_v

    return valid_layer_max_min(context.scene.sm_background) and valid_layer_max_min(context.scene.sm_foreground)


def color_division(color1, color2):
    return tuple([i / j for i, j in zip(color1, color2)])


def offset_power_slope(context):
    bg_layer = context.scene.sm_background
    fg_layer = context.scene.sm_foreground

    bg_slope = bg_layer.max_color - bg_layer.min_color
    fg_slope = fg_layer.max_color - fg_layer.min_color
    slope = color_division(bg_slope, fg_slope)

    bg_power = color_division(tuple(ti / 2 for ti in bg_slope), bg_layer.mid_color)
    fg_power = color_division(tuple(ti / 2 for ti in fg_slope), fg_layer.mid_color)
    power = color_division(bg_power, fg_power)

    offset = bg_layer.min_color - fg_layer.min_color
    basis = min(offset)
    offset = tuple([val - basis for val in list(offset)])

    return basis, offset, power, slope


def get_render_result(render_result):
    gpu_tex = gpu.texture.from_image(render_result)
    img = [x for row in gpu_tex.read() for pixel in row for x in list(pixel)]
    return img, gpu_tex.width, gpu_tex.height
