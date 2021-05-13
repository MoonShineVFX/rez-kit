
name = "six"

description = "Python 2 and 3 compatibility utilities"

version = "1.15.0-m1"

requires = []

variants = []

pip_packages = [
    "six==1.15.0",
]

private_build_requires = ["pipz"]
build_command = "install %s --bundle" % " ".join(pip_packages)


def commands():
    env = globals()["env"]

    env.PATH.prepend("{root}/bin")
    env.PYTHONPATH.prepend("{root}/python")
