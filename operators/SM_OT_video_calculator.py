import bpy
from ..utils import get_layer_settings, get_layer_name
from .op_utils import frame_analyze

class SM_OT_video_calculator(bpy.types.Operator):
    bl_idname = 'shot_matcher.video_calculator'
    bl_label = 'Video Color Analyzer'
    bl_description = 'Calculates the maximum/minimum values in a movie clip, following the frame range and step'
    bl_options = {'REGISTER', 'UNDO'}

    @classmethod
    def poll(cls, context):
        return get_layer_name(context) in bpy.data.movieclips
    
    def execute(self, context):
        context_layer = get_layer_settings(context)
        movie_clip = bpy.data.movieclips[get_layer_name(context)]

        if context_layer.start_frame < movie_clip.frame_start or context_layer.end_frame > movie_clip.frame_duration or context_layer.start_frame > context_layer.end_frame:
            self.report({'ERROR'}, 'Invalid frame range: it must be within the frame range of the video clip')
            return {'FINISHED'}
        
        context.window.cursor_set('WAIT')

        viewer_area = None
        viewer_space = None

        previousAreaType = None

        for area_search in bpy.context.screen.areas:
            if viewer_area == None and area_search.type == 'IMAGE_EDITOR':
                viewer_area = area_search
                break

        if viewer_area == None:
            viewer_area = bpy.context.screen.areas[0]
            previousAreaType = viewer_area.type
            viewer_area.type = 'IMAGE_EDITOR'

        for space in viewer_area.spaces:
            if space.type == 'IMAGE_EDITOR':
                viewer_space = space
        
        movie_image = bpy.data.images.load(movie_clip.filepath)
        viewer_space.image = movie_image

        #the frame_offset property starts at 0 index, so first frame is actually 0
        frame = context_layer.start_frame - 1
        frame_count = 0
        midtone_sum = (0.0,0.0,0.0)
        for frame in range(frame, context_layer.end_frame, context_layer.frame_step):  
            viewer_space.image_user.frame_offset = frame
            #switch back and forth to force refresh
            viewer_space.display_channels = 'COLOR'
            viewer_space.display_channels = 'COLOR_ALPHA'
            next_midtone = frame_analyze(context, movie_image, (frame == context_layer.start_frame - 1))
            midtone_sum = tuple(x + y for x, y in zip(midtone_sum, next_midtone))
            frame_count += 1
            self.report({'INFO'}, 'Shot Matcher: Analyzing frame {} for {}'.format(frame + 1, movie_image.name))
        # overwrite midtone color with average of all midtones
        context_layer.mid_color = tuple(ti / frame_count for ti in midtone_sum)
        
        context.window.cursor_set('DEFAULT')
        viewer_space.image = None
        if previousAreaType is not None:
            viewer_area.type = previousAreaType
            
        bpy.data.images.remove(movie_image)
        
        return {'FINISHED'}
