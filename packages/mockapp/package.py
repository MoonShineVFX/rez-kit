
early = globals()["early"]


@early()
def __mock():
    """Define package from command line option
    """
    import sys
    import argparse

    if any(help_ in sys.argv[1:] for help_ in ["-h", "--help"]):
        # Skip parsing version string if user is asking for help,
        # or the following parser will print out it's own help
        # message without rez-build's.
        return ""

    parser = argparse.ArgumentParser()

    with open("./parse_build_args.py", "r") as add_args:
        exec(add_args.read(), {"parser": parser})

    opt, unknown = parser.parse_known_args()  # parse `sys.argv`

    return {
        "name": opt.name,
        "version": opt.version,
        "requires": opt.requires or [],
        "tools": opt.tools or [],
    }


@early()
def name():
    mock = globals()["this"].__mock
    if mock:
        return "mock" + mock["name"]
    else:
        return "mockapp"


@early()
def description():
    mock = globals()["this"].__mock
    if mock:
        return "Mocking %s" % mock["name"]
    else:
        "Mocking App"


@early()
def version():
    mock = globals()["this"].__mock
    if mock:
        return mock["version"]
    else:
        return "0"


@early()
def requires():
    mock = globals()["this"].__mock
    if mock:
        return mock["requires"] + ["Qt.py"]  # for gui mock
    else:
        return []


@early()
def tools():
    mock = globals()["this"].__mock
    if mock:
        return mock["tools"]
    else:
        return []


@early()
def build_command():
    mock = globals()["this"].__mock
    command = "python {root}/rezbuild.py {install} "
    if mock:
        return command + " ".join(mock["tools"])
    else:
        return command


private_build_requires = [
    "identicon",
]


# This will be picked up by Allzpark
_data = {
    "icon": "{root}/resources/icon.png"
}


def commands():
    env = globals()["env"]

    env.PYTHONPATH.prepend("{root}/python")
    env.PATH.prepend("{root}/bin")
