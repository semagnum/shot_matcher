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


import bpy

from ..layers import build_layer_type
from .op_utils import get_render_result, valid_image


class SM_OT_color_picker(bpy.types.Operator):
    bl_idname = 'shot_matcher.color_picker'
    bl_description = 'Use a color picker to select the white and black values'
    bl_label = 'Min Max Color Picker'

    layer_type: bpy.props.StringProperty()

    def color_pick(self, context, event):
        if not valid_image(context.edit_image):
            self.report({'ERROR'}, 'Must have a valid image open in the image editor')
            return {'CANCELLED'}

        context_layer = self.context_layer

        mouse_x = event.mouse_x - context.region.x
        mouse_y = event.mouse_y - context.region.y
        uv = context.area.regions[-1].view2d.region_to_view(mouse_x, mouse_y)
        size_x, size_y = self.size_x, self.size_y
        x = int(size_x * uv[0]) % size_x
        y = int(size_y * uv[1]) % size_y
        offset = (y * size_x + x) * 4
        r, g, b, alpha = self.img_pixels[offset:offset + 4]
        if context_layer.use_alpha_threshold and context_layer.alpha_threshold > alpha:
            return {'RUNNING_MODAL'}

        # check max for each channel
        if r > context_layer.max_color[0]:
            context_layer.max_color[0] = r
        if g > context_layer.max_color[1]:
            context_layer.max_color[1] = g
        if b > context_layer.max_color[2]:
            context_layer.max_color[2] = b
            # check min for each channel
        if r < context_layer.min_color[0]:
            context_layer.min_color[0] = r
        if g < context_layer.min_color[1]:
            context_layer.min_color[1] = g
        if b < context_layer.min_color[2]:
            context_layer.min_color[2] = b
        context.area.tag_redraw()

    def modal(self, context, event):
        context.window.cursor_set('EYEDROPPER')

        context.area.header_text_set(text='LMB + drag: pick white/black colors, RMB: apply and finish, ESC: cancel')
        if event.type == 'LEFTMOUSE':  # start or end drag
            self.lmb = (event.value == 'PRESS')
        elif event.type == 'RIGHTMOUSE':  # accept color pick
            context.area.header_text_set(text=None)
            context.area.tag_redraw()
            context.window.cursor_set('DEFAULT')
            return {'FINISHED'}
        elif event.type == 'ESC':  # reset to original colors
            self.context_layer.min_color = (self.min_r, self.min_g, self.min_b)
            self.context_layer.max_color = (self.max_r, self.max_g, self.max_b)
            context.window.cursor_set('DEFAULT')
            context.area.header_text_set(text=None)
            context.area.tag_redraw()
            return {'FINISHED'}
        elif event.type in {'MIDDLEMOUSE', 'WHEELUPMOUSE', 'WHEELDOWNMOUSE'}:  # allow navigation shortcuts
            return {'PASS_THROUGH'}

        if self.lmb:
            self.color_pick(context, event)

        return {'RUNNING_MODAL'}

    def invoke(self, context, event):
        self.context_layer = build_layer_type(context, self.layer_type).settings
        self.lmb = False
        self.min_r = self.context_layer.min_color[0]
        self.min_g = self.context_layer.min_color[1]
        self.min_b = self.context_layer.min_color[2]
        self.max_r = self.context_layer.max_color[0]
        self.max_g = self.context_layer.max_color[1]
        self.max_b = self.context_layer.max_color[2]

        if context.area.type == 'IMAGE_EDITOR' and context.edit_image is not None:
            if context.edit_image.type == 'RENDER_RESULT':
                self.img_pixels, self.size_x, self.size_y = get_render_result(context.edit_image)
            else:
                self.img_pixels = context.edit_image.pixels
                self.size_x, self.size_y = context.edit_image.size[:]
            context.window_manager.modal_handler_add(self)
            return {'RUNNING_MODAL'}
        else:
            self.report({'WARNING'}, 'UV/Image Editor not found, cannot run operator')
            return {'CANCELLED'}
