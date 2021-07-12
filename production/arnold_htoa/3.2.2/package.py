
name = "arnold_htoa"

version = "3.2.2-m1"

_data = {
    # Allzpark
    "label": "HtoA",
    "icon": "{root}/htoa.ico"
}

requires = [
    "arnold_core-5.2.2.1",
    "~openvdb-4.0.0",
]

variants = [
    # ["platform-*", "houdini-16.5.634"],
    # ["platform-*", "houdini-17.0.416"],
    ["platform-*", "houdini-17.0.459"],
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
