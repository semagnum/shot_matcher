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


class SM_OT_set_selected(bpy.types.Operator):
    bl_idname = 'shot_matcher.set_selected'
    bl_label = 'Use Current Media'
    bl_description = 'Sets the layer to the current image/video shown'
    bl_options = {'REGISTER'}

    space_type: bpy.props.StringProperty()

    @classmethod
    def poll(cls, context):
        return (hasattr(context, 'edit_image') and hasattr(context.edit_image, 'name')) or (
                    hasattr(context, 'edit_movieclip') and hasattr(context.edit_movieclip, 'name'))

    def execute(self, context):
        if self.space_type == 'IMAGE_EDITOR':
            if context.scene.layer_context == 'bg':
                context.scene.sm_bg_name = context.edit_image.name
            else:
                context.scene.sm_fg_name = context.edit_image.name
        elif self.space_type == 'CLIP_EDITOR':
            if context.scene.layer_context == 'bg':
                context.scene.sm_bg_name = context.edit_movieclip.name
            else:
                context.scene.sm_fg_name = context.edit_movieclip.name
        else:
            return {'CANCELLED'}

        return {'FINISHED'}
