early = globals()["early"]

name = "rez"

description = "Rez itself as package"


@early()
def version():
    import os
    import rez

    os.environ["REZ_SOURCE_PATH"] = rez.__path__[0]

    # Our fork of rez has '+' sign in version string to indicate
    # local change.
    # Which align to PEP 440 version spec but not to rez package's
    # version syntax. So we have to normalize it.
    return rez.__version__.replace("+", "-")


variants = [
    ["platform-*", "arch-*", "os-*", "python-*.*"],
]

# NOTE: This build script is simply copying modules from rez source,
#       which is not robust. Better install with rez-kit deploy script.
build_command = "python {root}/rezbuild.py {install}"


def commands():
    env = globals()["env"]
    env.PYTHONPATH.append("{root}/payload")
