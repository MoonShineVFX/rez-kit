
name = "atomsbase"

version = "1.0-m1"

description = "Atoms Crowd generic environment setup"

build_command = False


def commands():
    env = globals()["env"]
    system = globals()["system"]
    resolve = globals()["resolve"]

    env.ATOMS_ROOT = "{root}"
    env.ATOMS_DATA = "{root}/data"
    env.ATOMS_FONTS = "{root}/fonts"
    env.ATOMS_GLSL_PATH = "{root}/glsl"
    env.ATOMS_GLSL_DISABLE_LIGHTS = "0"
    env.QT_PYTHON_API = "PySide2"

    # Maya

    if "maya" in resolve:
        # # ditch out maya module file, so we don't need to modify that after
        # # downloading newly released version.
        # #
        # # google this: Maya Distributing Multi-File Modules
        # #
        # env.MAYA_MODULE_PATH.prepend("{root}")

        if system.platform == "windows":
            env.PATH.prepend("{root}/bin")
            env.PATH.prepend("{root}/bin/${env.MAYA_VERSION}")
            env.PYTHONPATH.prepend("{root}/python/${env.MAYA_VERSION}")

        # plug-ins
        env.MAYA_PLUG_IN_PATH.prepend("{root}/plug-ins/${env.MAYA_VERSION}")
        # scripts
        env.PYTHONPATH.prepend("{root}/scripts")
        env.MAYA_SCRIPT_PATH.prepend("{root}/scripts")
        # presets
        env.MAYA_PRESET_PATH.prepend("{root}/presets")
        # icons
        env.XBMLANGPATH.prepend("{root}/icons")

        if "arnold_core" in resolve:
            env.ATOMSARNOLD_PROCEDURAL_PATH = (
                "{root}/arnold/${env.ARNOLD_CORE_VERSION}/${env.MAYA_VERSION}/"
                "procedural/AtomsArnoldProcedural.dll")
            env.ARNOLD_PLUGIN_PATH.prepend(
                "{root}/arnold/${env.ARNOLD_CORE_VERSION}/${env.MAYA_VERSION}/"
                "procedural")
            env.MTOA_EXTENSIONS_PATH.prepend(
                "{root}/arnold/${env.ARNOLD_CORE_VERSION}/${env.MAYA_VERSION}")

        if "redshift" in resolve:
            env.REDSHIFT_MAYAEXTENSIONSPATH.prepend(
                "{root}/redshift/${REZ_REDSHIFT_VERSION}/${env.MAYA_VERSION}")
            env.REDSHIFT_PROCEDURALSPATH.prepend(
                "{root}/redshift/${REZ_REDSHIFT_VERSION}/${env.MAYA_VERSION}/"
                "procedural")

        if "vray" in resolve:
            env.PATH.prepend(
                "{root}/vray/${env.VRAY_VERSION}/${env.MAYA_VERSION}"
            )
            env.MAYA_PLUG_IN_PATH.prepend(
                "{root}/vray/${env.VRAY_VERSION}/2017/${env.MAYA_VERSION}"
            )
            env.VRAY_PLUGINS_x64.prepend(
                "{root}/vray/${env.VRAY_VERSION}/2017"
            )
            env.VRAY_FOR_MAYA2017_PLUGINS_x64.prepend(
                "{root}/vray/${env.VRAY_VERSION}/${env.MAYA_VERSION}"
            )

        if "renderman" in resolve:
            env.ATOMS_RMAN_PROCEDURAL = (
                "{root}/rman/${RENDERMAN_VERSION}/${env.MAYA_VERSION}/"
                "AtomsRManProcedural.dll"
            )
            env.RFM_PLUGINS_PATH = (
                "{root}/rman/${RENDERMAN_VERSION}/${env.MAYA_VERSION}"
            )

        env.MAYA_RENDER_DESC_PATH.prepend("{root}/renderDesc")

    # Houdini

    if "houdini" in resolve:

        if system.platform == "windows":
            env.PATH.prepend("{root}/bin")
            env.PYTHONPATH.prepend("{root}/scripts")
        else:
            env.PYTHONPATH.prepend("{root}/scripts")
            env.PYTHONPATH.prepend("{root}/python")
            env.LD_LIBRARY_PATH.prepend("{root}/lib")

        env.HOUDINI_PATH.prepend("{root}")

        if "arnold_core" in resolve:
            env.ARNOLD_VERSION = "${env.ARNOLD_CORE_VERSION}"

        if "redshift" in resolve:
            pass

        if "renderman" in resolve:
            env.RMAN_VERSION = "${RENDERMAN_VERSION}"
