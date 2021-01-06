
name = "arnold_mtoa"

version = "3.0.1-m1"

_data = {
    # Allzpark
    "label": "MtoA",
    "icon": "{root}/SA.ico"
}

requires = [
    "arnold_core-5.1.1.0",
]

variants = [
    # ["platform-*", "maya-2016"],
    # ["platform-*", "maya-2016.5"],
    # ["platform-*", "maya-2017"],
    ["platform-*", "maya-2018"],
]

tools = [
    "kick",
    "oslc",
    "oslinfo",
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
