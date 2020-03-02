import bpy, sys
from ..LayerSettings import LayerSettings
from ..utils import get_layer_settings

class SM_OT_purge_layers(bpy.types.Operator):
    bl_idname = 'shot_matcher.purge_layers'
    bl_label = 'Purge Layers'
    bl_description = 'Deletes layer settings not matching any existing image/movie files in the blend file'
    bl_options = {'REGISTER', 'UNDO'}
    
    def execute(self, context):
        def purge_layer(settings_list):
            index = 0
            count = 0
            while index < len(settings_list):
                layer = settings_list[index]
                if (layer.settings.layer_type == 'image' and layer.name in bpy.data.images) or (layer.settings.layer_type == 'video' and layer.name in bpy.data.movieclips):
                    settings_list.remove(index)
                    count += 1
                else:
                    index +=1
            return count
        num_removed = purge_layer(context.scene.sm_settings_movieclips)
        num_removed += purge_layer(context.scene.sm_settings_images)
        self.report({'INFO'}, '{} settings have been removed'.format(num_removed))
        return {'FINISHED'}