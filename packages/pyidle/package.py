

name = "pyidle"

version = "1.0.0"

description = "Python IDLE"

requires = [
    "python"
]

tools = [
    "idle",
]

build_command = "python -m rezutil build {root}"
private_build_requires = ["rezutil-1"]


def commands():
    env = globals()["env"]

    env.PATH.prepend("{root}/bin")
    env.PYTHONPATH.prepend("{root}/python")
