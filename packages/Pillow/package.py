
name = "Pillow"

description = "Python Imaging Library (Fork)"

version = "7.2.0-m1"

requires = []

variants = [
    ["os", "python-3.7"],
]

pip_packages = [
    "Pillow==7.2.0",
]

private_build_requires = ["pipz"]
build_command = "install %s --bundle" % " ".join(pip_packages)


def commands():
    env = globals()["env"]

    env.PATH.prepend("{root}/bin")
    env.PYTHONPATH.prepend("{root}/python")
