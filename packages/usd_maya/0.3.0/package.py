
name = "usd_maya"

version = "0.3.0"

requires = [
    "python",
    "maya-2018+",
]

variants = [
    ["platform-*", "maya-2018", "python-2.7", "release-1"],
    ["platform-*", "maya-2020", "python-2.7", "release-1"],
    ["platform-*", "maya-2018", "python-2.7", "release-0"],
    ["platform-*", "maya-2020", "python-2.7", "release-0"],
]

build_requires = [
    "rezutil-1+",
    "cmake-3.2+",
    "usd-20.08",
    "maya_devkit",
    "qt-5",
    "future",  # for test
]
build_command = "python {root}/rezbuild.py {install}"


def commands():
    env = globals()["env"]

    env.MAYA_MODULE_PATH.append("{root}")
