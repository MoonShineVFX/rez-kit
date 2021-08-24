
name = "houdini"

version = "17.5.360-m5"

description = "SideFX Houdini"

_data = {
    # Allzpark
    "label": "Houdini",
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
