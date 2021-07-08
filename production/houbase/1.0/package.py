
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

    # Append "default" path for the given variable
    env.HOUDINI_PATH.append("&")
    env.HOUDINI_SCRIPT_PATH.append("&")

    # Expands to sub-dir of HOUDINI_PATH
    env.HOUDINI_MENU_PATH.append("@/")
    env.HOUDINI_OTLSCAN_PATH.append("@/otls")

    # version range specific
    if hou_version_info[:2] >= [17, 5]:
        env.PDG_USE_PDGNET = "1"
