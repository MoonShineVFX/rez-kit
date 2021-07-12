
name = "arnold_htoa"

version = "5.6.0.2-m1"

_data = {
    # Allzpark
    "label": "HtoA",
    "icon": "{root}/htoa.ico"
}

requires = [
    "arnold_core-6.2.0.1",
    "~usd_arnold-6.2.0.1",  # 67a96b94 (USD v20.11)
    "~openvdb-4.0.0",
]

variants = [
    ["platform-*", "houdini-18.0.597"],
    ["platform-*", "houdini-18.5.462"],
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
