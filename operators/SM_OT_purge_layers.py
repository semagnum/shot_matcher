import bpy, sys
from ..LayerSettings import LayerSettings
from ..utils import get_layer_settings

class SM_OT_purge_layers(bpy.types.Operator):
    bl_idname = 'shot_matcher.purge_layers'
    bl_label = 'Purge Layers'
    bl_description = 'Deletes layer settings not matching any existing image/movie files in the blend file'
    bl_options = {'REGISTER', 'UNDO'}
    
    def execute(self, context):
        def purge_layer(settings_list, data_list):
            index = 0
            nameList = []
            while index < len(settings_list):
                if settings_list[index].name not in data_list:
                    nameList.append(settings_list[index].name)
                    settings_list.remove(index)
                else:
                    index +=1
            return nameList
        names_removed = purge_layer(context.scene.sm_settings_movieclips, bpy.data.movieclips)
        names_removed = names_removed + purge_layer(context.scene.sm_settings_images, bpy.data.images)
        self.report({'INFO'}, '{} layer settings have been removed for the following images and movie clips:'.format(len(names_removed)))
        for name in names_removed:
            self.report({'INFO'}, name)
        return {'FINISHED'}