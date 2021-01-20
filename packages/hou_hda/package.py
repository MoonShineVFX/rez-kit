
name = "hou_hda"

version = "0.1.0-m1"

description = "Studio Houdini HDA collection"

requires = [
    "house-1.1+",
    "houdini",
]

build_command = False


def commands():
    env = globals()["env"]

    env.HOUDINI_OTLSCAN_PATH.prepend("$HOUSE_HOUDINI_HDA")
    env.HOUDINI_MENU_PATH.prepend("$HOUSE_HOUDINI_HDA")
