
name = "houdini"

version = "18.0.597-m2"

description = "SideFX Houdini"

_data = {
    # Allzpark
    "label": "Houdini 18.0.597",
    "icon": "{root}/resources/icon.svg"
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
