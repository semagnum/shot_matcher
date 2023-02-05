import bpy

from .SM_PT_image_analyzer import SM_PT_image_analyzer
from .SM_PT_video_analyzer import SM_PT_video_analyzer

_register_order = [SM_PT_image_analyzer, SM_PT_video_analyzer]


def register():
    for cls in _register_order:
        bpy.utils.register_class(cls)


def unregister():
    for cls in _register_order[::-1]:
        bpy.utils.unregister_class(cls)
