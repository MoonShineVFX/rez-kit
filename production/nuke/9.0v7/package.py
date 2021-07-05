
name = "nuke"

version = "9.0v7-m1"

description = "The Foundry Nuke 9.0v7"

_data = {
    # Allzpark
    "label": "Nuke",
    "icon": "{root}/resources/nuke.ico"
}


@early()
def requires():
    if building:
        return []
    else:
        return ["!PySide2"]


tools = [
    "nukex",
    "nuke",
]


private_build_requires = ["rezutil-1"]
build_command = "python -m rezutil build {root}"


def commands():
    env = globals()["env"]
    alias = globals()["alias"]
    system = globals()["system"]

    env.NUKE_VERSION = str(env.REZ_NUKE_VERSION).rsplit("-m", 1)[0]

    if system.platform == "windows":
        env.NUKE_LOCATION = "C:/Program Files/Nuke{env.NUKE_VERSION}"

        alias("nuke", "Nuke9.0")
        alias("nukex", "Nuke9.0 -x")

    elif system.platform == "linux":
        pass

    elif system.platform == "osx":
        pass

    env.PATH.append("{env.NUKE_LOCATION}")
