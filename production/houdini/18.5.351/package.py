
name = "houdini"

version = "18.5.351-m3"

description = "SideFX Houdini"

_data = {
    "label": "Houdini 18.5.351",
    "icon": "{root}/resources/icon.svg",
    "level": "task",
    "role": None,
}

requires = [
    "!PySide2",
    "houbase-1",
]

tools = [
    "houdinifx",
]


private_build_requires = ["rezutil-1"]
build_command = "python -m rezutil build {root}"
