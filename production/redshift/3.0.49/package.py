
name = "redshift"

version = "3.0.49-m4"

_data = {
    # Allzpark
    "label": "Redshift",
    "icon": "{root}/logo.svg"
}

requires = [
    "~maya-2014+<2023",
    "~houdini-"
    "17.0.506|17.5.460|"
    "18.0.597|"
    "18.5.532|18.5.563|18.5.596",
]

variants = [
    ["platform-*"],
]

private_build_requires = ["rezutil-1"]
build_command = "python -m rezutil build {root} --use-zip"


def commands():
    env = globals()["env"]
    resolve = globals()["resolve"]

    env.REDSHIFT_VERSION = str(env.REZ_REDSHIFT_VERSION).rsplit("-m", 1)[0]

    # Important:
    #   The foundation of all other redshift env vars
    #
    env.REDSHIFT_COREDATAPATH = "{root}"

    if "maya" in resolve:
        env.PATH.prepend("{root}/bin")

        # plug-ins
        env.MAYA_PLUG_IN_PATH.prepend(
            "{root}/Plugins/Maya/{env.MAYA_VERSION}/nt-x86-64")
        # scripts
        env.PYTHONPATH.prepend(
            "{root}/Plugins/Maya/Common/scripts")
        env.MAYA_SCRIPT_PATH.prepend(
            "{root}/Plugins/Maya/Common/scripts")
        # icons
        env.XBMLANGPATH.prepend(
            "{root}/Plugins/Maya/Common/icons")

        env.MAYA_CUSTOM_TEMPLATE_PATH.prepend(
            "{root}/Plugins/Maya/Common/scripts/NETemplates")
        env.REDSHIFT_MAYAEXTENSIONSPATH.prepend(
            "{root}/Plugins/Maya/{env.MAYA_VERSION}/nt-x86-64/extensions")
        env.REDSHIFT_PROCEDURALSPATH.prepend(
            "{root}/Procedurals")

    if "houdini" in resolve:
        env.PATH.prepend("{root}/bin")
        env.HOUDINI_PATH.prepend("{root}/Plugins/Houdini/${HOUDINI_VERSION}")
        env.PXR_PLUGINPATH_NAME.append("{root}/Plugins/Solaris/${HOUDINI_VERSION}")
        env.HOUDINI_DSO_ERROR = "2"
