
name = "houdini"

version = "18.5.532-m4"

description = "SideFX Houdini"

_data = {
    "label": "Houdini 18.5.532",
    "icon": "{root}/resources/icon.svg",
    "level": "task",
    "role": None,
}

requires = [
    "!PySide2",
    "hou_base-1",
]

tools = [
    "houdinifx",
]


private_build_requires = ["rezutil-1"]
build_command = "python -m rezutil build {root}"
