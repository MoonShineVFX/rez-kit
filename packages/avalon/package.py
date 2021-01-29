

name = "avalon"

version = "0.0.0-m0"

github_repo = "MoonShineVFX/avalon-core"  # for rez-deliver


def preprocess(this, data):
    import os

    # These two environment variables should be set by our
    # 'github-based Rez package releasing tool' -> rez-deliver
    #
    payload_ver = "GITHUB_REZ_PKG_PAYLOAD_VER"
    release_path = "REZ_RELEASE_PACKAGES_PATH"

    if os.getenv(payload_ver):
        data["version"] = "%s-%s" % (
            # payload version
            os.environ[payload_ver],
            # package def version
            "m1"
        )

    if os.getenv(release_path):
        try:
            _ = data["config"]["release_packages_path"]
        except KeyError:
            data["config"] = data["config"] or {}
            data["config"]["release_packages_path"] = os.environ[release_path]
        else:
            pass  # already explicitly specified by package


def pre_build_commands():
    env = globals()["env"]
    this = globals()["this"]
    env.GITHUB_REPO = this.github_repo


requires = [
    "house",
    "pymongo",
    "Qt.py",
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


def pre_commands():
    env = globals()["env"]

    # (NOTE) convert it into `list` or it will always return True when
    #   checking __contains__.
    #   >>> "anything" in env.keys()
    #   True
    #   >>> "anything" in list(env.keys())
    #   False
    #
    current_env_keys = list(env.keys())

    env.AVALON_SESSION_SCHEMA = "avalon-core:session-3.0"
    session_v3_required = [
        "AVALON_PROJECTS",
        "AVALON_PROJECT",
        "AVALON_CONFIG",
    ]
    for key in session_v3_required:
        if key not in current_env_keys:
            env[key] = "__placeholder__"


# Set up environment
def commands():
    env = globals()["env"]
    resolve = globals()["resolve"]
    env.PYTHONPATH.prepend("{root}/payload")

    # MongoDB
    env.AVALON_MONGO = "{env.HOUSE_PIPELINE_MONGO}"
    env.AVALON_DB = "avalon"
    env.AVALON_TIMEOUT = 5000

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

    # Avalon application toml
    # (for file copying and creating default dirs)
    env.PATH.prepend("{root}/apps")
    # Avalon tools
    env.PATH.prepend("{root}/bin")
    # Allzpark env plugin (Avalon launcher)
    env.PYTHONPATH.prepend("{root}/python")


def post_commands():
    import os
    env = globals()["env"]
    resolve = globals()["resolve"]

    # Ozark setup
    if "ozark" in resolve:
        # Register location 'avalon' to mongozark
        env.REZ_CONFIG_FILE.append("{root}/config/rezconfig.py")
        env.ALLZPARK_CONFIG_FILE = "{root}/config/allzparkconfig.py"
        # Avalon profile template
        env.REZ_OZARK_TEMPLATE = "{root}/template"

    # (NOTE) convert it into `list` or it will always return True when
    #   checking __contains__.
    #   >>> "anything" in env.keys()
    #   True
    #   >>> "anything" in list(env.keys())
    #   False
    #
    current_env_keys = list(env.keys())

    # Startup workdir
    required = [
        "AVALON_PROJECTS",
        "AVALON_PROJECT",
        "AVALON_APP",
    ]
    if all(k in current_env_keys for k in required):
        env.AVALON_WORKDIR = os.path.sep.join([
            "{env.AVALON_PROJECTS}",
            "{env.AVALON_PROJECT}",
            "Avalon",
            "_Lobby",
            "{env.AVALON_APP}",
        ])
