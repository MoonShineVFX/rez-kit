
name = "arnold_htoa"

version = "5.2.1-m1"

_data = {
    # Allzpark
    "label": "HtoA",
    "icon": "{root}/htoa.ico"
}

requires = [
    "arnold_core-6.0.3.0",
    "~openvdb-4.0.0",
    "~usd_arnold-6.0.3.0",  # 2056d6bf (!=6.0.3.0)
]

variants = [
    # ["platform-*", "houdini-17.0.506"],
    ["platform-*", "houdini-17.5.460"],
    ["platform-*", "houdini-18.0.416"],
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
