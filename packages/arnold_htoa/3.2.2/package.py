
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
    # ["platform", "houdini-16.5.634"],
    # ["platform", "houdini-17.0.416"],
    ["platform", "houdini-17.0.459"],
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


def commands():
    env = globals()["env"]

    env.PATH.append("{root}/scripts/bin")
    env.HOUDINI_PATH.prepend("{root}")

    env.HTOA_STARTUP_LOG = "0"
    env.HOUDINI_DSO_ERROR = "2"

    # Dev use
    # env.HOUDINI_SCRIPT_DEBUG = "1"
    # env.HOUDINI_SOHO_DEVELOPER = "1"

    # Force using houdini built-in python
    # env.HOUDINI_USE_HFS_PYTHON = "1"

    # Use default browser on the system to open the help URLs (windows)
    # env.HOUDINI_EXTERNAL_HELP_BROWSER = "start"

    # Modifying individual HOUDINI_*_PATHs
    #
    # If you have already used the individual HOUDINI_*_PATH environments for
    # other plugins and scripts, you may find you need to set them for HtoA
    # instead of using only the HOUDINI_PATH environment.
    #
    # In case you also set one of the following environment variables, make
    # sure you are appending ";@;&", at the end of its value, or alternatively,
    # add the corresponding HtoA subfolder path to it:
    #
    # env.HOUDINI_DSO_PATH = "{root}/dso"
    # env.HOUDINI_OTLSCAN_PATH = "{root}/otls"
    # env.HOUDINI_SCRIPT_PATH = "{root}/scripts"
    # env.HOUDINI_SOHO_PATH.prepend("{root}/soho")
    # env.HOUDINI_TOOLBAR_PATH = "{root}/toolbar"
    # env.HOUDINI_UI_ICON_PATH = "{root}/config/Icons"
    # env.HOUDINI_UI_PATH = "{root}/config"
