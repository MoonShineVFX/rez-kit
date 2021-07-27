
name = "redshift"

version = "3.0.34-m3"

_data = {
    # Allzpark
    "label": "Redshift",
    "icon": "{root}/logo.svg"
}

requires = [
    "~maya-2014+<2021",
    "~houdini-"
    "17.0.506|17.5.460|"
    "18.0.532|18.0.566|18.0.597|"
    "18.5.351|18.5.408",
]

variants = [
    ["platform-*"],
]

private_build_requires = ["rezutil-1"]
build_command = "python -m rezutil build {root} --use-zip"


def commands():
    env = globals()["env"]
    resolve = globals()["resolve"]

    # Important:
    #   The foundation of all other redshift env vars
    #
    env.REDSHIFT_COREDATAPATH = "{root}"

    if "maya" in resolve:
        env.MAYA_MODULE_PATH.prepend("{root}")

    if "houdini" in resolve:
        env.PATH.prepend("{root}/bin")
        env.HOUDINI_PATH.prepend("{root}/Plugins/Houdini/${HOUDINI_VERSION}")
        env.PXR_PLUGINPATH_NAME.append("{root}/Plugins/Solaris/${HOUDINI_VERSION}")
        env.HOUDINI_DSO_ERROR = "2"
