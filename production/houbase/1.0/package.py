
name = "houbase"

version = "1.0-m5"

description = "SideFX Houdini generic environment setup"

build_command = False


def pre_commands():
    import os

    env = globals()["env"]
    stop = globals()["stop"]
    system = globals()["system"]
    resolve = globals()["resolve"]
    building = globals()["building"]

    def env_version_split(env_var):  # no pkg ver
        return [int(t) for t in str(env_var).rsplit("-")[0].split(".")]

    def is_dependent_in_context(dep_name):
        return (dep_name in resolve
                or (building and env.REZ_BUILD_PROJECT_NAME == dep_name))

    if not is_dependent_in_context("houdini"):
        stop("Package 'houdini' is not in context. "
             "Houdini executable path cannot be composed.")

    if building and str(env.REZ_BUILD_PROJECT_NAME) == "houdini":
        hou_version_info = env_version_split(env.REZ_BUILD_PROJECT_VERSION)
    else:
        hou_version_info = env_version_split(env.REZ_HOUDINI_VERSION)

    hou_version_str = "{}.{}.{}".format(*hou_version_info)

    if system.platform == "windows":
        hou_root = ("C:/Program Files/Side Effects Software/Houdini %s"
                    % hou_version_str)

    elif system.platform == "linux":
        hou_root = ""
        stop("Houdini %s installed location root not set." % hou_version_str)

    elif system.platform == "osx":
        hou_root = ""
        stop("Houdini %s installed location root not set." % hou_version_str)

    else:
        hou_root = ""
        stop("Unknown system platform.")

    env.HOUDINI_ROOT = hou_root
    env.HOUDINI_VERSION = hou_version_str

    # check py3 via $HHP (the path to Houdini’s python libraries)
    #   notice that even houdini is not been built with py3, it may still
    #   have `python3.7libs` folder. need to check the content for sure.
    py3_feature = os.path.join(hou_root, "houdini", "python3.7libs", "hou.py")
    if os.path.isfile(py3_feature):
        env.HOUDINI_PY3_BUILD = "1"


def commands():
    env = globals()["env"]

    env.PATH.append("{env.HOUDINI_ROOT}/bin")

    # Disable local .env file
    env.HOUDINI_NO_ENV_FILE = "1"

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

    # Disable anonymous usage statistics collection entirely.
    env.HOUDINI_ANONYMOUS_STATISTICS = "0"

    # version range specific
    hou_version_info = [int(v) for v in str(env.HOUDINI_VERSION).split(".")]

    if hou_version_info[:2] >= [17, 5]:
        env.PDG_USE_PDGNET = "1"


def post_commands():
    env = globals()["env"]

    env.HOUDINI_PATH.append("&")

    hou_env = {
        "HOUDINI_DSO_PATH":         "@/dso",
        "HOUDINI_GLSL_PATH":        "@/ogl2",
        "HOUDINI_MENU_PATH":        "@",
        "HOUDINI_OCL_PATH":         "@/ocl",
        "HOUDINI_OTLSCAN_PATH":     "@/otls",
        "HOUDINI_TOOLBAR_PATH":     "@/toolbar",
        "HOUDINI_SOHO_PATH":        "@/soho",
        "HOUDINI_SCRIPT_PATH":      "@/scripts",
        "HOUDINI_UI_PATH":          "@/config",
        "HOUDINI_UI_ICON_PATH":     "@/config/Icons",
        "HOUDINI_VEX_PATH":         "@/vex",
    }
    for key, sub_dir in hou_env.items():
        if key in env:
            # Expands to sub-dir of HOUDINI_PATH
            env[key].append(sub_dir)
            # Append "default" path for the given variable
            env[key].append("&")
