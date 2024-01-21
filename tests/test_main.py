import math
import os
from pathlib import Path
import pytest

import bpy
import addon_utils

from tests.util import load_image, load_video


def get_zip_file_in_parent_dir():
    """Gets first zip file it can find.

    Since this will be in the tests/ folder,
    we need to go up a folder to find the zip file.
    """
    parent_dir = Path(os.getcwd()).parent
    for root, dirs, files in os.walk(parent_dir):
        for file in files:
            if file.endswith(".zip"):
                return os.path.join(root, file)

    raise FileNotFoundError('No zip file to install into Blender!')


@pytest.fixture(scope="session", autouse=True)
def install_addon(request):
    """Installs the addon for testing. After the session is finished, it optionally deletes the registered add-on."""
    bpy.ops.preferences.addon_install(filepath=get_zip_file_in_parent_dir())

    addon_utils.modules_refresh()
    bpy.ops.script.reload()

    bpy.ops.preferences.addon_enable(module='shot_matcher')

    yield

    # In my case (using symlinks), since this add-on is already enabled,
    # this installs the add-on twice.
    # So I need to delete the newly installed add-on folder afterward.

    import os
    import shutil
    if os.getenv('ADDON_INSTALL_PATH_TO_REMOVE') is not None:
        shutil.rmtree(os.getenv('ADDON_INSTALL_PATH_TO_REMOVE'))


@pytest.fixture
def context():
    import bpy
    return bpy.context

@pytest.fixture
def data():
    import bpy
    return bpy.data


@pytest.fixture
def ops():
    import bpy
    # bpy module doesn't refresh the scene per test,
    # so I need to reload the file each time
    bpy.ops.wm.read_homefile()
    return bpy.ops


def test_sanity():
    """If this fails, you are probably not setup, period ;P."""
    assert 1 + 1 == 2


def assert_color(actual_color, expected_color):
    assert all(math.isclose(av, ev, abs_tol=0.0001) for av, ev in zip(actual_color, expected_color))


def test_reset_color_picker(context, data, ops):
    load_image(context, data, ops)
    ops.shot_matcher.color_reset(layer_type='target')


def test_image_analysis(context, data, ops):
    load_image(context, data, ops)

    ops.shot_matcher.image_calculator(layer_type='target')

    background = context.scene.sm_background
    assert_color(background.max_color, (1.0, 1.0, 1.0))
    assert_color(background.mid_color, (0.3058, 0.3174, 0.3264))
    assert_color(background.min_color, (0.0, 0.0, 0.0))


def test_color_balance_node(context, data, ops):
    load_image(context, data, ops)

    ops.shot_matcher.image_calculator(layer_type='target')
    ops.shot_matcher.color_balance_node()


def test_alpha_over_node(context, data, ops):
    load_image(context, data, ops)

    ops.shot_matcher.image_calculator(layer_type='target')
    ops.shot_matcher.alpha_over_node()


def test_video_analysis(context, data, ops):
    load_video(context, data, ops)

    context.scene.sm_foreground.frame_step = 100

    ops.shot_matcher.video_calculator(layer_type='source')
    ops.shot_matcher.video_frame_calculator(layer_type='source')
