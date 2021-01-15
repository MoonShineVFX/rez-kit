
name = "pymongo"

description = "Python driver for MongoDB <http://www.mongodb.org>"

version = "3.11.0-m1"

requires = []

variants = [
    ["os", "python-2.7"],
    ["os", "python-3.7"],
]

pip_packages = [
    "pymongo==3.11.0",
]

private_build_requires = ["pipz"]
build_command = "install %s --bundle" % " ".join(pip_packages)


def commands():
    env = globals()["env"]

    env.PATH.prepend("{root}/bin")
    env.PYTHONPATH.prepend("{root}/python")
