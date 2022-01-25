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
