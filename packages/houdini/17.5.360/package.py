
name = "houdini"

version = "17.5.360-m1"

description = "SideFX Houdini"

_data = {
    # Allzpark
    "label": "Houdini",
    "icon": "{root}/resources/icon.svg"
}

requires = [
    "!PySide2",
]

tools = [
    "houdinifx",
]


private_build_requires = ["rezutil-1"]
build_command = "python -m rezutil build {root}"


def commands():
    env = globals()["env"]
    alias = globals()["alias"]
    system = globals()["system"]

    # strip out Rez package version
    hou_version = str(env.REZ_HOUDINI_VERSION).rsplit(".", 1)[0]
    env.HOUDINI_VERSION = hou_version

    if system.platform == "windows":
        env.HOUDINI_LOCATION = "C:/Program Files/Side Effects Software/"\
                               "Houdini {env.HOUDINI_VERSION}"

        env.HOUDINI_SCRIPT_PATH.append("{env.HOUDINI_LOCATION}/houdini/scripts")
        env.HOUDINI_OTLSCAN_PATH.append("@/otls")
        env.HOUDINI_MENU_PATH.append("@/")

        # When start dir is at root drive e.g. "F:", OTLs may fail to load
        # on startup with errors like:
        #   "ImportError: No module named sidefx_stroke"
        alias("houdinifx", "start /d %USERPROFILE% houdinifx")

    elif system.platform == "linux":
        pass

    elif system.platform == "osx":
        pass

    env.PATH.append("{env.HOUDINI_LOCATION}/bin")
    env.PDG_USE_PDGNET = "1"

    # Disable local .env file
    env.HOUDINI_NO_ENV_FILE = "1"

    # Append "default" path for the given variable
    env.HOUDINI_PATH.append("&")
