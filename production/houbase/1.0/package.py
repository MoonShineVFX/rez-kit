
name = "houbase"

version = "1.0-m1"

description = "SideFX Houdini generic environment setup"

build_command = False


def commands():
    env = globals()["env"]
    stop = globals()["stop"]
    alias = globals()["alias"]
    system = globals()["system"]
    resolve = globals()["resolve"]

    if "houdini" not in resolve:
        stop("Package 'houdini' is not in resolves. "
             "Houdini executable path cannot be composed.")

    hou_version_info = [
        int(t) for t in
        resolve["houdini"].version.as_tuple()[:3]  # no pkg ver
    ]
    env.HOUDINI_VERSION = "{}.{}.{}".format(*hou_version_info)

    if system.platform == "windows":
        env.HOUDINI_LOCATION = "C:/Program Files/Side Effects Software/"\
                               "Houdini {env.HOUDINI_VERSION}"

        # When start dir is at root drive e.g. "F:", OTLs may fail to load
        # on startup with errors like:
        #   "ImportError: No module named sidefx_stroke"
        alias("houdinifx", "start /d %USERPROFILE% houdinifx")

    elif system.platform == "linux":
        pass

    elif system.platform == "osx":
        pass

    env.PATH.append("{env.HOUDINI_LOCATION}/bin")

    # Disable local .env file
    env.HOUDINI_NO_ENV_FILE = "1"

    # Expands to sub-dir of HOUDINI_PATH
    env.HOUDINI_MENU_PATH.append("@")
    env.HOUDINI_VEX_PATH.append("@/vex")
    env.HOUDINI_OCL_PATH.append("@/ocl")
    env.HOUDINI_GLSL_PATH.append("@/ogl2")
    env.HOUDINI_OTLSCAN_PATH.append("@/otls")

    # Append "default" path for the given variable
    env.HOUDINI_PATH.append("&")
    env.HOUDINI_DSO_PATH.append("&")
    env.HOUDINI_SOHO_PATH.append("&")
    env.HOUDINI_SCRIPT_PATH.append("&")
    env.HOUDINI_OTLSCAN_PATH.append("&")
    env.HOUDINI_TOOLBAR_PATH.append("&")
    env.HOUDINI_UI_PATH.append("&")
    env.HOUDINI_UI_ICON_PATH.append("&")

    # Force using houdini built-in python (deprecated)
    # env.HOUDINI_USE_HFS_PYTHON = "1"

    # Dev use, enables more verbose console output
    # env.HOUDINI_SCRIPT_DEBUG = "1"
    # env.HOUDINI_SOHO_DEVELOPER = "1"

    # Use default browser on the system to open the help URLs (windows)
    # env.HOUDINI_EXTERNAL_HELP_BROWSER = "start"

    # Determines if DSO/DLL errors on plug-ins will be printed out to
    # the console.
    # "1" : dynamic linking errors to be output
    # "2" : more verbose errors to be printed
    # "3" : all DSO related messages to be printed
    # "4" : timing messages to be printed
    # env.HOUDINI_DSO_ERROR = "2"

    # version range specific
    if hou_version_info[:2] >= [17, 5]:
        env.PDG_USE_PDGNET = "1"
