
name = "arnold_htoa"

version = "4.2.0-m1"

_data = {
    # Allzpark
    "label": "HtoA",
    "icon": "{root}/htoa.ico"
}

requires = [
    "arnold_core-5.4.0.0",
    "~openvdb-4.0.0",
]

variants = [
    # ["platform-*", "houdini-16.5.634"],
    # ["platform-*", "houdini-17.0.506"],
    # ["platform-*", "houdini-17.5.327"],
    ["platform-*", "houdini-17.5.360"],
]

tools = [
    "hick",
    "kick",
    "oslc",
    "oslinfo",
    "oiiotool",
    "maketx",
    "noice",
]


private_build_requires = ["rezutil-1"]
build_command = "python -m rezutil build {root} --use-zip"
