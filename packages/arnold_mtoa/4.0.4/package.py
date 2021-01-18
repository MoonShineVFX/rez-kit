
name = "arnold_mtoa"

version = "4.0.4-m1"

_data = {
    # Allzpark
    "label": "MtoA",
    "icon": "{root}/arnold.ico"
}

requires = [
    "arnold_core-6.0.4.0",
]

variants = [
    ["platform-*", "maya-2018"],
    # ["platform-*", "maya-2019"],
    ["platform-*", "maya-2020"],
]

tools = [
    "kick",
    "oslc",
    "oslinfo",
    "oiiotool",
    "maketx",
    "noice",
]


private_build_requires = ["rezutil-1"]
build_command = "python -m rezutil build {root} --use-zip"


def commands():
    env = globals()["env"]

    env.PATH.append("{root}/bin")
    env.MAYA_MODULE_PATH.append("{root}/modules")
    env.ARNOLD_PLUGIN_PATH.append("{root}/shaders")
    env.MTOA_STARTUP_LOG_VERBOSITY = "1"
