
name = "arnold_mtoa"

version = "3.3.0-m2"

_data = {
    # Allzpark
    "label": "MtoA",
    "icon": "{root}/SA.ico"
}

requires = [
    "arnold_core-5.4.0.0",
]

variants = [
    # ["platform-*", "maya-2017"],
    ["platform-*", "maya-2018"],
    # ["platform-*", "maya-2019"],
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

    env.PATH.prepend("{root}/bin")
    env.MAYA_SCRIPT_PATH.prepend("{root}/scripts/mtoa/mel")
    env.MAYA_CUSTOM_TEMPLATE_PATH.prepend("{root}/scripts/mtoa/ui/templates")
    env.MAYA_RENDER_DESC_PATH.prepend("{root}")
    env.ARNOLD_PLUGIN_PATH.prepend("{root}/shaders")
    env.MTOA_STARTUP_LOG_VERBOSITY = "1"
