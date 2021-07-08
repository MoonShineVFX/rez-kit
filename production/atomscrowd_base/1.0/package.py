
name = "atomscrowd_base"

version = "1.0-m1"

description = "Atoms Crowd generic environment setup"

build_command = False


def commands():
    env = globals()["env"]
    system = globals()["system"]
    resolve = globals()["resolve"]

    # Maya

    if "maya" in resolve:
        env.MAYA_MODULE_PATH.prepend("{root}")

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
            # env.PATH.prepend("{root}/vray/3.60/2017")
            # env.MAYA_PLUG_IN_PATH.prepend("{root}/vray/3.60/2017/maya")
            # env.VRAY_PLUGINS_x64.prepend("{root}/vray/3.60/2017")
            # env.VRAY_FOR_MAYA2017_PLUGINS_x64.prepend("{root}/vray/3.60/2017")
            pass

        if "renderman" in resolve:
            # env.ATOMS_RMAN_PROCEDURAL = "rman/22.6/2018/AtomsRManProcedural.dll"
            # env.RFM_PLUGINS_PATH = "rman/22.6/2018"
            pass

    # Houdini

    if "houdini" in resolve:

        env.ATOMS_ROOT = "{root}"
        env.ATOMS_DATA = "{root}/data"
        env.ATOMS_FONTS = "{root}/fonts"
        env.ATOMS_GLSL_PATH = "{root}/glsl"

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
            # env.RMAN_VERSION = "21.5"
            pass
