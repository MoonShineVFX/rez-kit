
name = "PySide2"

description = "Python bindings for the Qt cross-platform application " \
              "and UI framework"

version = "5.15-m1"

requires = []

variants = [
    ["os", "python-3.7"],
]

pip_packages = [
    "PySide2==5.15",
    "shiboken2==5.15",
]

private_build_requires = ["pipz"]
build_command = "install %s --bundle" % " ".join(pip_packages)


def commands():
    env = globals()["env"]

    env.PATH.prepend("{root}/bin")
    env.PYTHONPATH.prepend("{root}/python")
