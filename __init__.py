import bpy

from .LayerSettings import LayerSettings
from .LayerDict import LayerDict
from .utils import type_update, get_bg_name, get_fg_name, set_bg_name, set_fg_name, copy_settings
from bpy.app.handlers import persistent

from .operators.SM_OT_color_picker import SM_OT_color_picker
from .operators.SM_OT_color_reset import SM_OT_color_reset
from .operators.SM_OT_alpha_over_node import SM_OT_alpha_over_node
from .operators.SM_OT_color_balance_node import SM_OT_color_balance_node
from .operators.SM_OT_image_calculator import SM_OT_image_calculator
from .operators.SM_OT_set_selected import SM_OT_set_selected
from .operators.SM_OT_video_calculator import SM_OT_video_calculator
from .operators.SM_OT_video_frame_calculator import SM_OT_video_frame_calculator

from .panels.SM_PT_image_analyzer import SM_PT_image_analyzer
from .panels.SM_PT_video_analyzer import SM_PT_video_analyzer

bl_info = {
    "name": 'Shot Matcher',
    "author": 'Spencer Magnusson',
    "version": (3, 4, 4),
    "blender": (2, 83, 0),
    "description": 'Analyzes colors of an image or movie clip and applies it to the compositing tree.',
    "location": 'Image Editor > UI > Shot Matcher & Movie Clip Editor > Tools > Shot Matcher',
    "support": 'COMMUNITY',
    "category": 'Compositing'
}

model_classes = [LayerSettings, LayerDict]

addon_classes = [
    SM_OT_color_picker, SM_OT_color_reset,
    SM_OT_alpha_over_node, SM_OT_color_balance_node,
    SM_OT_image_calculator,
    SM_OT_set_selected,
    SM_OT_video_calculator, SM_OT_video_frame_calculator,
    SM_PT_image_analyzer, SM_PT_video_analyzer
]


@persistent
def save_pre_layer_settings(dummy):
    def save_layer(scene, layer_name, sm_layer, sm_layer_type):
        if layer_name == '':
            return

        if sm_layer_type == 'video':
            layer_dict = scene.sm_settings_movieclips
        else:
            layer_dict = scene.sm_settings_images

        current_index = layer_dict.find(layer_name)
        copy_settings(sm_layer, layer_dict[current_index].setting)

    for scene in bpy.data.scenes:
        save_layer(scene, scene.sm_bg_name, scene.sm_background, scene.sm_bg_type)
        save_layer(scene, scene.sm_fg_name, scene.sm_foreground, scene.sm_fg_type)


@persistent
def load_post_purge_settings(dummy):
    def purge_layer(settings_list, data_list, print_type):
        index = 0
        name_list = []
        while index < len(settings_list):
            if settings_list[index].name not in data_list:
                name_list.append(settings_list[index].name)
                settings_list.remove(index)
            else:
                index += 1
        if len(name_list) > 0:
            print('{} layer settings have been removed for the following {}:'.format(len(name_list), print_type))
            for name in name_list:
                print('\t{}'.format(name))

    for scene in bpy.data.scenes:
        purge_layer(scene.sm_settings_movieclips, bpy.data.movieclips, 'movieclips')
        purge_layer(scene.sm_settings_images, bpy.data.images, 'images')


def register():
    for cls in model_classes:
        bpy.utils.register_class(cls)

    scene = bpy.types.Scene
    scene.sm_settings_movieclips = bpy.props.CollectionProperty(type=LayerDict)
    scene.sm_settings_images = bpy.props.CollectionProperty(type=LayerDict)
    scene.sm_fg_type = bpy.props.EnumProperty(
        name='Layer Type',
        description='Select which file type the foreground layer is',
        items=[('video', 'Video', '', 'FILE_MOVIE', 1),
               ('image', 'Image', '', 'FILE_IMAGE', 2),
               ],
        update=type_update
    )
    scene.sm_bg_type = bpy.props.EnumProperty(
        name='Layer Type',
        description='Select which file type the background layer is',
        items=[('video', 'Video', '', 'FILE_MOVIE', 1),
               ('image', 'Image', '', 'FILE_IMAGE', 2),
               ],
        update=type_update
    )
    scene.layer_context = bpy.props.EnumProperty(
        name='Layer',
        description='The current layer being analyzed',
        items=[('bg', 'Background', ''),
               ('fg', 'Foreground', ''),
               ]
    )
    scene.sm_background = bpy.props.PointerProperty(type=LayerSettings)
    scene.sm_foreground = bpy.props.PointerProperty(type=LayerSettings)
    scene.sm_bg_name = bpy.props.StringProperty(default='', get=get_bg_name, set=set_bg_name)
    scene.sm_fg_name = bpy.props.StringProperty(default='', get=get_fg_name, set=set_fg_name)

    bpy.app.handlers.save_pre.append(save_pre_layer_settings)
    bpy.app.handlers.load_post.append(load_post_purge_settings)

    for cls in addon_classes:
        bpy.utils.register_class(cls)


def unregister():
    for cls in addon_classes[::-1]:
        bpy.utils.unregister_class(cls)
    scene = bpy.types.Scene

    bpy.app.handlers.save_pre.remove(save_pre_layer_settings)
    bpy.app.handlers.load_post.remove(load_post_purge_settings)
    
    del scene.sm_settings_movieclips, scene.sm_settings_images, scene.sm_bg_type, scene.sm_fg_type
    del scene.sm_background, scene.sm_foreground, scene.layer_context

    for cls in model_classes[::-1]:
        bpy.utils.unregister_class(cls)
