
name = "houdini"

version = "18.0.566-m1"

description = "SideFX Houdini"

_data = {
    # Allzpark
    "label": "Houdini 18.0.566",
    "icon": "{root}/resources/icon.svg"
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
