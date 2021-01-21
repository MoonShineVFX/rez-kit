early = globals()["early"]

name = "rez"

description = "Rez itself as package"


@early()
def version():
    import os
    import rez

    os.environ["REZ_SOURCE_PATH"] = rez.__path__[0]

    return rez.__version__


variants = [
    ["platform-*", "arch-*", "os-*", "python-2.*"],
    ["platform-*", "arch-*", "os-*", "python-3.*"],
]

# NOTE: This build script is simply copying modules from rez source,
#       which is not robust. Better install with rez-kit deploy script.
build_command = "python {root}/rezbuild.py {install}"


def commands():
    env = globals()["env"]
    env.PYTHONPATH.append("{root}/payload")
