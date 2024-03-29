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
from .op_utils import frame_analyze


class SM_OT_video_frame_calculator(bpy.types.Operator):
    bl_idname = 'shot_matcher.video_frame_calculator'
    bl_label = 'Video Frame Color Analyzer'
    bl_description = 'Calculates the maximum/minimum values for a single movie clip frame'
    bl_options = {'REGISTER', 'UNDO'}

    layer_type: bpy.props.StringProperty()

    def findImageEditor(self):
        self.viewer_area = None
        self.viewer_space = None
        self.previousAreaType = None

        for area_search in bpy.context.screen.areas:
            if self.viewer_area is None and area_search.type == 'IMAGE_EDITOR':
                self.viewer_area = area_search
                break

        if self.viewer_area is None:
            self.viewer_area = bpy.context.screen.areas[0]
            self.previousAreaType = self.viewer_area.type
            self.viewer_area.type = 'IMAGE_EDITOR'

        for space in self.viewer_area.spaces:
            if space.type == 'IMAGE_EDITOR':
                self.viewer_space = space

    def cancelCleanup(self, context, message):
        self.report({'ERROR'}, message)
        context.window.cursor_set('DEFAULT')
        try:
            bpy.data.images.remove(self.movie_image)
        except Exception:
            pass
        return {'CANCELLED'}

    def execute(self, context):
        layer = build_layer_type(context, self.layer_type)
        if layer.name not in bpy.data.movieclips:
            self.report({'ERROR'}, 'Must have a valid movieclip selected')
            return {'CANCELLED'}

        movie_clip = bpy.data.movieclips[layer.name]

        curr_frame = context.scene.frame_current

        if curr_frame < movie_clip.frame_start or curr_frame > movie_clip.frame_duration:
            return self.cancelCleanup(context=context,
                                      message='Invalid frame: it must be within the frame range of the video clip')

        context.window.cursor_set('WAIT')

        self.findImageEditor()

        self.movie_image = bpy.data.images.load(movie_clip.filepath)
        self.viewer_space.image = self.movie_image

        # the frame_offset property starts at 0 index, so first frame is actually 0
        frame = curr_frame - 1
        self.viewer_space.image_user.frame_duration = movie_clip.frame_duration
        self.viewer_space.image_user.frame_current = frame

        # switch back and forth to force refresh
        self.viewer_space.display_channels = 'COLOR'
        self.viewer_space.display_channels = 'COLOR_ALPHA'
        frame_analyze(self.viewer_space.image.pixels, layer.settings)

        self.viewer_space.image = None
        if self.previousAreaType is not None:
            self.viewer_area.type = self.previousAreaType

        return {'FINISHED'}
