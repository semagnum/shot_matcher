import bpy
from ..utils import frame_analyze

class SM_OT_video_calculator(bpy.types.Operator):
    bl_idname = "color_matching_analyzer.video_calculator"
    bl_label = "Video Color Analyzer"
    bl_description = "Calculates the maximum/minimum values in a movie clip, following the frame range and step"
    bl_options = {'REGISTER', 'UNDO'}

    layer = None
    
    @classmethod
    def poll(cls, context):
        return layer is not None and layer.layer_name
    
    def execute(self, context):
        
        movie_clip = bpy.data.movieclips[layer.layer_name]

        if layer.start_frame < movie_clip.frame_start or layer.end_frame > movie_clip.frame_duration or layer.start_frame > layer.end_frame:
            self.report({'ERROR'}, "Invalid frame range: it must be within the frame range of the video clip")
            return {'FINISHED'}
        
        context.window.cursor_set("WAIT")

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
            viewer_area.type = "IMAGE_EDITOR"

        for space in viewer_area.spaces:
            if space.type == "IMAGE_EDITOR":
                viewer_space = space

        viewer_space.image = bpy.data.images.load(movie_clip.filepath)

        #the frame_offset property starts at 0 index, so first frame is actually 0
        frame = layer.start_frame - 1
        for frame in range(frame, layer.end_frame, layer.frame_step):  
            viewer_space.image_user.frame_offset = frame
            #switch back and forth to force refresh
            viewer_space.display_channels = 'COLOR'
            viewer_space.display_channels = 'COLOR_ALPHA'
            frame_analyze(context, viewer_space.image, (frame == layer.start_frame - 1))
            self.report({'INFO'}, "Analyzing frame {}".format(frame + 1))

        viewer_space.image.user_clear()
        bpy.data.images.remove(viewer_space.image)        
        
        context.window.cursor_set("DEFAULT")
        if previousAreaType is not None:
            viewer_area.type = previousAreaType
        
        return {'FINISHED'}
