
late = globals()["late"]


name = "avalon"

description = "The safe post-production pipeline"

git_url = "https://github.com/MoonShineVFX/avalon-core.git"


@early()
def version():
    import os

    package_ver = "m1"
    payload_ver = os.getenv("REZ_DELIVER_PKG_PAYLOAD_VER")

    if payload_ver:
        return "%s-%s" % (
            # payload version
            payload_ver,
            # package def version
            package_ver
        )

    else:
        return "0.0.0-" + package_ver


def pre_build_commands():
    env = globals()["env"]
    expandvars = globals()["expandvars"]
    optionvars = globals()["optionvars"]

    feature = expandvars("{this.name}.dev")
    env.REZ_BUILD_PKG_PAYLOAD_ROOT = optionvars(feature, default="")


requires = [
    "house",
    "pymongo",
    "Qt.py",
    "pyblish",
    "pyblish_qml",
]

private_build_requires = ["rezutil-1"]
build_command = "python {root}/rezbuild.py {install}"

_data = {
    "label": "Avalon",
    "icon": "{root}/payload/res/icons/ico/avalon.ico"
}


@late()
def tools():
    in_context = globals()["in_context"]
    # Avalon tools
    _tools = [
        "loader",
    ]

    if in_context():
        context = globals()["context"]
        for pkg in context.resolved_packages:
            if getattr(pkg, "is_project_admin", False):
                _tools.append("manager")
                break

    return _tools


# Set up environment
def commands():
    env = globals()["env"]
    resolve = globals()["resolve"]

    # DCC App Setup
    if "maya" in resolve:
        env.PYTHONPATH.append("{root}/payload/setup/maya")
        env.AVALON_APP = "maya"
        env.AVALON_APP_NAME = "maya"

    if "houdini" in resolve:
        env.HOUDINI_SCRIPT_PATH.append("{root}/payload/res/houdini")
        env.AVALON_APP = "houdini"
        env.AVALON_APP_NAME = "houdini"

    if "nuke" in resolve:
        env.NUKE_PATH.append("{root}/payload/setup/nuke/nuke_path")
        env.AVALON_APP = "nuke"
        env.AVALON_APP_NAME = "nuke"

    # Avalon tools
    env.PATH.prepend("{root}/bin")
    # Avalon payload
    env.PYTHONPATH.prepend("{root}/payload")
    # Allzpark
    env.ALLZPARK_CONFIG_FILE = "{root}/config/allzparkconfig.py"

    # MongoDB (pkg 'house' required)
    env.AVALON_MONGO = "{env.HOUSE_PIPELINE_MONGO}"
    env.AVALON_DB = "avalon"
    env.AVALON_TIMEOUT = 5000
