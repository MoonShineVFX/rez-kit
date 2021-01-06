
name = "future"

description = "Clean single-source support for Python 3 and 2"

version = "0.18.2-m1"

requires = []

variants = [
    ["python-2.7"],
]

pip_packages = [
    "future==0.18.2",
]

private_build_requires = ["pipz"]
build_command = "install %s --bundle" % " ".join(pip_packages)


def commands():
    env = globals()["env"]

    env.PATH.prepend("{root}/bin")
    env.PYTHONPATH.prepend("{root}/python")
