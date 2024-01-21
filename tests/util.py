import os


def load_image(context, data, ops):
    image_path = os.path.join(os.path.abspath('..'), 'docs', 'assets', 'img', 'shot-matcher-logo.png')
    img = data.images.load(image_path)

    context.scene.sm_bg_type = 'image'

    with context.temp_override(edit_image=img):
        ops.shot_matcher.set_selected(space_type='IMAGE_EDITOR', layer_type='target')

def load_video(context, data, ops):
    video_path = os.environ['TEST_VIDEO_PATH']
    if video_path is None:
        raise ValueError('Must have "TEST_VIDEO_PATH" environment variable set')
    clip = data.movieclips.load(video_path)

    context.scene.sm_bg_type = 'video'

    with context.temp_override(edit_movieclip=clip):
        ops.shot_matcher.set_selected(space_type='CLIP_EDITOR', layer_type='source')