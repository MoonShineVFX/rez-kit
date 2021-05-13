
name = "hou_hda"

version = "0.1.0-m1"

description = "Studio Houdini HDA collection"

requires = [
    "houdini",
]

build_command = False


def commands():
    env = globals()["env"]

    env.HOUDINI_OTLSCAN_PATH.prepend("Q:/Resource/houdini")
    env.HOUDINI_MENU_PATH.prepend("Q:/Resource/houdini")
