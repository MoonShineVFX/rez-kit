
name = "atomscrowd"

version = "2.8.1-m1"

_data = {
    # Allzpark
    "label": "AtomsCrowd",
    "icon": "{root}/logo.png"
}

requires = [
    "~arnold_core-5.2.2.1|5.3.0.2",
]

variants = [
    ["platform-*", "maya"],
    # ["platform-*", "houdini-17.5.229"],
]

private_build_requires = ["rezutil-1"]
build_command = "python -m rezutil build {root} --use-zip"


def commands():
    env = globals()["env"]
    resolve = globals()["resolve"]

    if "maya" in resolve:
        env.MAYA_MODULE_PATH.prepend("{root}")

        # arnold
        if "arnold_core" in resolve:
            env.ATOMSARNOLD_PROCEDURAL_PATH = (
                "{root}/arnold/${REZ_ARNOLD_CORE_VERSION}/${REZ_MAYA_VERSION}/"
                "procedural/AtomsArnoldProcedural.dll")
            env.ARNOLD_PLUGIN_PATH.prepend(
                "{root}/arnold/${REZ_ARNOLD_CORE_VERSION}/${REZ_MAYA_VERSION}/"
                "procedural")
            env.MTOA_EXTENSIONS_PATH.prepend(
                "{root}/arnold/${REZ_ARNOLD_CORE_VERSION}/${REZ_MAYA_VERSION}")

        # redshift
        if "redshift" in resolve:
            env.REDSHIFT_MAYAEXTENSIONSPATH.prepend(
                "{root}/redshift/${REZ_REDSHIFT_VERSION}/${REZ_MAYA_VERSION}")
            env.REDSHIFT_PROCEDURALSPATH.prepend(
                "{root}/redshift/${REZ_REDSHIFT_VERSION}/${REZ_MAYA_VERSION}/"
                "procedural")

        # vray
        # env.PATH.prepend("{root}/vray/3.60/2017")
        # env.MAYA_PLUG_IN_PATH.prepend("{root}/vray/3.60/2017/maya")
        # env.VRAY_PLUGINS_x64.prepend("{root}/vray/3.60/2017")
        # env.VRAY_FOR_MAYA2017_PLUGINS_x64.prepend("{root}/vray/3.60/2017")

        # renderman
        # env.ATOMS_RMAN_PROCEDURAL = "rman/22.6/2018/AtomsRManProcedural.dll"
        # env.RFM_PLUGINS_PATH = "rman/22.6/2018"

    if "houdini" in resolve:
        env.PATH.prepend("{root}/bin")
        env.PYTHONPATH.prepend("{root}/scripts")
        env.HOUDINI_PATH.prepend("{root}")
        env.ATOMS_ROOT = "{root}"
        env.ATOMS_DATA = "{root}/data"
        env.ATOMS_FONTS = "{root}/fonts"
        env.ATOMS_GLSL_PATH = "{root}/glsl"

        # arnold
        if "arnold_core" in resolve:
            env.ARNOLD_VERSION = "${REZ_ARNOLD_CORE_VERSION}"

        # renderman
        # env.RMAN_VERSION = "21.5"
