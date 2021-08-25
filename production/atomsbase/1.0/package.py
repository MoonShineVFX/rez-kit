
name = "atomsbase"

version = "1.0-m7"

description = "Atoms Crowd generic environment setup"

build_command = False


def pre_commands():
    env = globals()["env"]
    stop = globals()["stop"]
    resolve = globals()["resolve"]
    building = globals()["building"]

    def is_dependent_in_context(dep_name):
        return (dep_name in resolve
                or (building and env.REZ_BUILD_PROJECT_NAME == dep_name))

    if not is_dependent_in_context("atomsvfx") \
            and not is_dependent_in_context("atomscrowd"):
        stop("No atoms-crowd package resolved for setting 'ATOMS_ROOT' var.")

    if "atomsvfx" in resolve:
        env.ATOMS_ROOT = "{env.REZ_ATOMSVFX_ROOT}"
        env.ATOMS_VERSION = "{env.REZ_ATOMSVFX_VERSION}".rsplit("-m", 1)[0]

    elif "atomscrowd" in resolve:
        env.ATOMS_ROOT = "{env.REZ_ATOMSCROWD_ROOT}"
        env.ATOMS_VERSION = "{env.REZ_ATOMSCROWD_VERSION}".rsplit("-m", 1)[0]

    else:  # is building 'atomsvfx' or 'atomscrowd'
        env.ATOMS_ROOT = "%s/%s" % (env.REZ_BUILD_PATH,
                                    env.REZ_BUILD_VARIANT_SUBPATH)
        env.ATOMS_VERSION = \
            str(env.REZ_BUILD_PROJECT_VERSION).rsplit("-m", 1)[0]


def commands():
    import os

    env = globals()["env"]
    stop = globals()["stop"]
    system = globals()["system"]
    resolve = globals()["resolve"]

    env.ATOMS_DATA = "{env.ATOMS_ROOT}/data"
    env.ATOMS_FONTS = "{env.ATOMS_ROOT}/fonts"
    env.ATOMS_GLSL_PATH = "{env.ATOMS_ROOT}/glsl"
    env.ATOMS_GLSL_DISABLE_LIGHTS = "0"
    env.QT_PYTHON_API = "PySide2"

    # Disables the fallback to higher priority licenses.
    #   So when there are no procedural license for rendering, won't fallback
    #   to use framework/simulation license which often still be needed in
    #   production time.
    env.TOOLCHEFS_DISABLE_FORCE_LICENSE = "1"

    # Maya

    if "maya" in resolve:
        # # ditch out maya module file, so we don't need to modify that after
        # # downloading newly released version.
        # #
        # # google this: Maya Distributing Multi-File Modules
        # #
        # env.MAYA_MODULE_PATH.prepend("{root}")

        if system.platform == "windows":
            env.PATH.prepend(
                "{env.ATOMS_ROOT}/bin")
            env.PATH.prepend(
                "{env.ATOMS_ROOT}/bin/{env.MAYA_VERSION}")
            env.PYTHONPATH.prepend(
                "{env.ATOMS_ROOT}/python/{env.MAYA_VERSION}")

        # plug-ins
        env.MAYA_PLUG_IN_PATH.prepend(
            "{env.ATOMS_ROOT}/plug-ins/{env.MAYA_VERSION}")
        # scripts
        env.PYTHONPATH.prepend(
            "{env.ATOMS_ROOT}/scripts")
        env.MAYA_SCRIPT_PATH.prepend(
            "{env.ATOMS_ROOT}/scripts")
        # presets
        env.MAYA_PRESET_PATH.prepend(
            "{env.ATOMS_ROOT}/presets")
        # icons
        env.XBMLANGPATH.prepend(
            "{env.ATOMS_ROOT}/icons")

        if "arnold_core" in resolve:
            env.ATOMSARNOLD_PROCEDURAL_PATH = (
                "{env.ATOMS_ROOT}/arnold/{env.ARNOLD_CORE_VERSION}/"
                "{env.MAYA_VERSION}/procedural/AtomsArnoldProcedural.dll")
            env.ARNOLD_PLUGIN_PATH.prepend(
                "{env.ATOMS_ROOT}/arnold/{env.ARNOLD_CORE_VERSION}/"
                "{env.MAYA_VERSION}/procedural")
            env.MTOA_EXTENSIONS_PATH.prepend(
                "{env.ATOMS_ROOT}/arnold/{env.ARNOLD_CORE_VERSION}/"
                "{env.MAYA_VERSION}")

        if "redshift" in resolve:
            env.REDSHIFT_MAYAEXTENSIONSPATH.prepend(
                "{env.ATOMS_ROOT}/redshift/${REDSHIFT_VERSION}/"
                "{env.MAYA_VERSION}")
            env.REDSHIFT_PROCEDURALSPATH.prepend(
                "{env.ATOMS_ROOT}/redshift/${REDSHIFT_VERSION}/"
                "{env.MAYA_VERSION}/procedural")

        if "vray" in resolve:
            env.PATH.prepend(
                "{env.ATOMS_ROOT}/vray/{env.VRAY_VERSION}/"
                "{env.MAYA_VERSION}")
            env.MAYA_PLUG_IN_PATH.prepend(
                "{env.ATOMS_ROOT}/vray/{env.VRAY_VERSION}/"
                "{env.MAYA_VERSION}/maya")
            env.VRAY_PLUGINS_x64.prepend(
                "{env.ATOMS_ROOT}/vray/{env.VRAY_VERSION}/"
                "{env.MAYA_VERSION}")

        if "renderman" in resolve:
            env.ATOMS_RMAN_PROCEDURAL = (
                "{env.ATOMS_ROOT}/rman/${RENDERMAN_VERSION}/"
                "{env.MAYA_VERSION}/AtomsRManProcedural.dll")
            env.RFM_PLUGINS_PATH = (
                "{env.ATOMS_ROOT}/rman/${RENDERMAN_VERSION}/"
                "{env.MAYA_VERSION}")

        env.MAYA_RENDER_DESC_PATH.prepend("{env.ATOMS_ROOT}/renderDesc")

    # Houdini

    if "houdini" in resolve:
        # Here we check for whether Atoms is for Houdini Python3 build
        #
        #   The difference between Atoms-Houdini Py2 & Py3 build is the .pyd
        #   module contains binary string 'python3'. We chose to check with
        #   `_AtomsModules.pyd` is because it's the smallest file (33kb).
        #
        #   The first Python 3 build supported Atoms version is 4.3.0,
        #   for Houdini 18.5.633.
        #
        atoms_root = str(env.ATOMS_ROOT)
        atoms_pyd = os.path.join(atoms_root, "scripts", "_AtomsModules.pyd")
        if os.path.isfile(atoms_pyd):
            with open(atoms_pyd, "rb") as f:
                is_py3_build = b"python3" in f.read()

            if is_py3_build and "HOUDINI_PY3_BUILD" not in env:
                stop("Python 3 built Atoms [%s] cannot work with "
                     "Python 2 built Houdini [%s]."
                     % (env.ATOMS_VERSION, resolve["houdini"].version))

        if system.platform == "windows":
            env.PATH.prepend("{env.ATOMS_ROOT}/bin")
            env.PYTHONPATH.prepend("{env.ATOMS_ROOT}/scripts")
        else:
            env.PYTHONPATH.prepend("{env.ATOMS_ROOT}/scripts")
            env.PYTHONPATH.prepend("{env.ATOMS_ROOT}/python")
            env.LD_LIBRARY_PATH.prepend("{env.ATOMS_ROOT}/lib")

        env.HOUDINI_PATH.prepend("{env.ATOMS_ROOT}")

        if "arnold_core" in resolve:
            env.ARNOLD_VERSION = "{env.ARNOLD_CORE_VERSION}"

        if "redshift" in resolve:
            pass

        if "renderman" in resolve:
            env.RMAN_VERSION = "${RENDERMAN_VERSION}"
