import bpy

from ..operators.SM_OT_purge_layers import SM_OT_purge_layers

class SM_PT_unused_layers(bpy.types.Panel):
    bl_space_type = 'IMAGE_EDITOR'
    bl_label = "Unused Layer Settings"
    bl_category = "Shot Matcher"
    bl_region_type = 'UI'

    def get_disconnected(self, layer_dict, data_list):
        return len([layer.name for layer in layer_dict if layer.name not in data_list])
    
    def draw(self, context):
        layout = self.layout
        movie_list = self.get_disconnected(context.scene.sm_settings_movieclips, bpy.data.movieclips)
        image_list = self.get_disconnected(context.scene.sm_settings_images, bpy.data.images)
        if len(movie_list) > 0:
            layout.label(text='The following movie layer settings cannot find their respective movie clips:')
            for movie_name in movie_list:
                layout.label(text='* {}'.format(movie_name))
        else:
            layout.label(text='All layer settings are connected to their respective movie clips')
        if len(image_list) > 0:
            layout.label(text='The following image layer settings cannot find their respective image clips:')
            for image_name in image_list:
                layout.label(text='* {}'.format(image_name))
        else:
            layout.label(text='All layer settings are connected to their respective images')
        layout.operator(SM_OT_purge_layers.bl_idname, text='Purge Unused Layer Settings')