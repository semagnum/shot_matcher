import bpy
from ..utils import frame_analyze

class CMA_OT_video_calculator(bpy.types.Operator):
    bl_idname = "color_matching_analyzer.video_calculator"
    bl_label = "Video Color Analyzer"
    bl_options = {'REGISTER', 'UNDO'}
    
    @classmethod
    def poll(cls, context):
        return context.edit_movieclip is not None and context.scene.cma_start_frame >= context.edit_movieclip.frame_start and context.scene.cma_end_frame <= context.edit_movieclip.frame_duration
    
    def execute(self, context):
        
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

        path = context.edit_movieclip.filepath
        viewer_space.image = bpy.data.images.load(path)

        #the frame_offset property starts at 0 index, so first frame is actually 0
        frame = context.scene.cma_start_frame - 1
        for frame in range(frame, context.scene.cma_end_frame, context.scene.cma_frame_step):  
            viewer_space.image_user.frame_offset = frame
            #switch back and forth to force refresh
            viewer_space.draw_channels = 'COLOR'
            viewer_space.draw_channels = 'COLOR_ALPHA'
            frame_analyze(context, viewer_space.image, (frame == context.scene.cma_start_frame - 1))
            self.report({'INFO'}, "Analyzing frame {}".format(frame + 1))

        viewer_space.image.user_clear()
        bpy.data.images.remove(viewer_space.image)        
        
        context.window.cursor_set("DEFAULT")
        if previousAreaType is not None:
            viewer_area.type = previousAreaType
        
        return {'FINISHED'}