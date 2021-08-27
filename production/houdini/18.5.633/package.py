
name = "houdini"

version = "18.5.633-m1"

description = "SideFX Houdini"

_data = {
    "label": "Houdini 18.5.633",
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
    "hython",
]


private_build_requires = ["rezutil-1"]
build_command = "python -m rezutil build {root}"
