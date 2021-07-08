
name = "houdini"

version = "18.0.460-m4"

description = "SideFX Houdini"

_data = {
    # Allzpark
    "label": "Houdini",
    "icon": "{root}/resources/icon.svg"
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
