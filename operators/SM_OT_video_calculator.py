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


class SM_OT_video_calculator(bpy.types.Operator):
    bl_idname = 'shot_matcher.video_calculator'
    bl_label = 'Video Color Analyzer'
    bl_description = 'Calculates the maximum/minimum values in a movie clip, following the frame range and step'
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

    def resetUI(self):
        self.viewer_space.image = None
        if self.previousAreaType is not None:
            self.viewer_area.type = self.previousAreaType

    def cancelCleanup(self, context, message, reset_ui=False):
        self.report({'ERROR'}, message)
        context.window.cursor_set('DEFAULT')
        if reset_ui:
            self.resetUI()
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

        context_layer = layer.settings
        movie_clip = bpy.data.movieclips[layer.name]

        if context_layer.start_frame < movie_clip.frame_start or context_layer.end_frame > movie_clip.frame_duration or context_layer.start_frame > context_layer.end_frame:
            return self.cancelCleanup(context=context,
                                      message='Invalid frame range: it must be within the frame range of the video clip')

        context.window.cursor_set('WAIT')

        self.findImageEditor()

        self.movie_image = bpy.data.images.load(movie_clip.filepath)
        self.viewer_space.image = self.movie_image

        # the frame_offset property starts at 0 index, so first frame is actually 0
        frame = context_layer.start_frame - 1
        all_images = []
        self.viewer_space.image_user.frame_duration = movie_clip.frame_duration
        for frame in range(frame, context_layer.end_frame, context_layer.frame_step):
            self.viewer_space.image_user.frame_current = frame
            # switch back and forth to force refresh
            self.viewer_space.display_channels = 'COLOR'
            self.viewer_space.display_channels = 'COLOR_ALPHA'
            try:
                all_images.append(self.viewer_space.image.pixels)
            except MemoryError:
                return self.cancelCleanup(context=context,
                                          message='Memory overload, analysis failed (lessen the frame range)',
                                          reset_ui=True)

        self.resetUI()
        try:
            frame_analyze(all_images, layer.settings)
        except MemoryError:
            return self.cancelCleanup(context=context,
                                      message='Memory overload, analysis failed (lessen the frame range)')

        return {'FINISHED'}
