import bpy

from .op_utils import frame_analyze
from ..utils import get_layer_name


class SM_OT_video_frame_calculator(bpy.types.Operator):
    bl_idname = 'shot_matcher.video_frame_calculator'
    bl_label = 'Video Frame Color Analyzer'
    bl_description = 'Calculates the maximum/minimum values for a single movie clip frame'
    bl_options = {'REGISTER', 'UNDO'}

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

    @classmethod
    def poll(cls, context):
        return get_layer_name(context) in bpy.data.movieclips

    def execute(self, context):
        movie_clip = bpy.data.movieclips[get_layer_name(context)]

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
        frame_analyze(context, self.viewer_space.image.pixels)

        self.viewer_space.image = None
        if self.previousAreaType is not None:
            self.viewer_area.type = self.previousAreaType

        return {'FINISHED'}
