
name = "PySide"

description = "Python bindings for the Qt cross-platform application " \
              "and UI framework"

version = "1.2.4-m1"

requires = []

variants = [
    ["os", "python-2.7"],
]

pip_packages = [
    "PySide==1.2.4",
    "shiboken==1.2.2",
]

private_build_requires = ["pipz"]
build_command = "install %s --bundle" % " ".join(pip_packages)


def commands():
    env = globals()["env"]

    env.PATH.prepend("{root}/bin")
    env.PYTHONPATH.prepend("{root}/python")
