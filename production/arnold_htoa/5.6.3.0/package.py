
name = "arnold_htoa"

version = "5.6.3.0-m1"

_data = {
    # Allzpark
    "label": "HtoA",
    "icon": "{root}/htoa.ico"
}

requires = [
    "arnold_core-6.2.1.1",
    "~usd_arnold-6.2.1.1",  # 67a96b94 (USD v20.11)
    "~openvdb-4.0.0",
]

variants = [
    ["platform-*", "houdini-17.5.460"],
    ["platform-*", "houdini-18.0.597"],
    ["platform-*", "houdini-18.5.596"],
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
