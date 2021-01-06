
name = "PyOpenGL"

description = "Standard OpenGL bindings for Python"

version = "3.1.5-m1"

requires = []

variants = [
    ["python-2.7"],
    ["python-3.7"],
]

pip_packages = [
    "PyOpenGL==3.1.5",
]

private_build_requires = ["pipz"]
build_command = "install %s --bundle" % " ".join(pip_packages)


def commands():
    env = globals()["env"]

    env.PATH.prepend("{root}/bin")
    env.PYTHONPATH.prepend("{root}/python")
