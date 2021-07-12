
name = "arnold_base"

version = "1.0-m1"

build_command = False


def pre_commands():
    env = globals()["env"]
    resolve = globals()["resolve"]

    if "arnold_core" in resolve:
        env.ARNOLD_CORE_VERSION = \
            str(env.REZ_ARNOLD_CORE_VERSION).rsplit("-m", 1)[0]


def commands():
    env = globals()["env"]
    resolve = globals()["resolve"]

    if "arnold_mtoa" in resolve:
        env.MTOA_ROOT = "{env.REZ_ARNOLD_MTOA_ROOT}"

        env.PATH.prepend(
            "{env.MTOA_ROOT}/bin")
        env.MAYA_SCRIPT_PATH.prepend(
            "{env.MTOA_ROOT}/scripts/mtoa/mel")
        env.MAYA_CUSTOM_TEMPLATE_PATH.prepend(
            "{env.MTOA_ROOT}/scripts/mtoa/ui/templates")
        env.MAYA_RENDER_DESC_PATH.prepend(
            "{env.MTOA_ROOT}")
        env.ARNOLD_PLUGIN_PATH.prepend(
            "{env.MTOA_ROOT}/shaders")
        env.MTOA_STARTUP_LOG_VERBOSITY = \
            "1"

    if "arnold_htoa" in resolve:
        env.HTOA_ROOT = "{env.REZ_ARNOLD_HTOA_ROOT}"

        env.PATH.prepend("{env.HTOA_ROOT}/scripts/bin")
        env.HOUDINI_PATH.prepend("{env.HTOA_ROOT}")

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
        env.HOUDINI_DSO_PATH.prepend(
            "{env.HTOA_ROOT}/dso")
        env.HOUDINI_SCRIPT_PATH.prepend(
            "{env.HTOA_ROOT}/scripts")
        env.HOUDINI_OTLSCAN_PATH.prepend(
            "{env.HTOA_ROOT}/otls")
        env.HOUDINI_SOHO_PATH.prepend(
            "{env.HTOA_ROOT}/soho")
        env.HOUDINI_TOOLBAR_PATH.prepend(
            "{env.HTOA_ROOT}/toolbar")
        env.HOUDINI_UI_PATH.prepend(
            "{env.HTOA_ROOT}/config")
        env.HOUDINI_UI_ICON_PATH.prepend(
            "{env.HTOA_ROOT}/config/Icons")

        # "0" : disable the shader registration log messages at startup
        env.HTOA_STARTUP_LOG = "0"
