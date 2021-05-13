

name = "pyblish_qml"

description = "Pyblish QML frontend for Maya 2013+, Houdini 11+, " \
              "Nuke 8+ and more"

version = "1.11.4p-m1"


authors = [
    "Marcus Ottosson",
    "Toke Jepsen",
    "David Lai",
    "davidlatwe",
    "Roy Nieterau",
    "nasefbasdf",
    "Alan Fregtman",
    "Jasper van Nieuwenhuizen",
    "Lars van der Bijl",
    "davidpower",
    "linez69",
    "Renaud Lessard Larouche",
    "liorbenhorin",
    "unknown",
    "Coyode",
    "Felix Yan",
    "Yamahigashi",
]


tools = [
]

requires = [
    "pyblish",
    "Qt.py",
]


private_build_requires = ["rezutil-1"]
build_command = "python {root}/rezbuild.py {install}"


# Set up environment
def commands():
    import os
    import subprocess
    env = globals()["env"]

    env.PYTHONPATH.prepend("{root}/payload/lib")

    # Get python executable path for Pyblish finding python and pyqt5
    # This is for Houdini.

    environ = os.environ.copy()
    environ["PATH"] = str(env.PATH.value())
    result = subprocess.check_output(["where", "python"], env=environ)
    result = result.decode()
    python_exec = result.split("\n")[0].strip()

    env.PYBLISH_QML_PYTHON_EXECUTABLE = python_exec
