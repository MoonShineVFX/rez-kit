early = globals()["early"]

name = "rezgui"

description = "Rez GUI App"


@early()
def version():
    import os
    import rez

    os.environ["REZ_SOURCE_PATH"] = rez.__path__[0]

    return rez.__version__


tools = [
    "rez-gui",
]

requires = [
    "rez",
    "Qt.py",
]

variants = [
    ["platform-*"],
]

build_command = "python {root}/rezbuild.py {install}"


def commands():
    env = globals()["env"]
    env.PYTHONPATH.append("{root}/payload")
    env.PATH.append("{root}/payload/bin")
