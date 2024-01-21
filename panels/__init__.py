import bpy

from .ImageEditor import SM_PT_image_analyzer_source, SM_PT_image_analyzer_target, SM_PT_image_analyzer_apply
from .MovieClipEditor import SM_PT_video_analyzer_source, SM_PT_video_analyzer_target, SM_PT_video_analyzer_apply
from .Compositor import SM_PT_compositor_source, SM_PT_compositor_target, SM_PT_compositor_apply

_register_order = [SM_PT_image_analyzer_target, SM_PT_image_analyzer_source, SM_PT_image_analyzer_apply,
                   SM_PT_video_analyzer_target, SM_PT_video_analyzer_source, SM_PT_video_analyzer_apply,
                   SM_PT_compositor_source, SM_PT_compositor_target, SM_PT_compositor_apply]


def register():
    for cls in _register_order:
        bpy.utils.register_class(cls)


def unregister():
    for cls in _register_order[::-1]:
        bpy.utils.unregister_class(cls)
