
name = "paramiko"

description = "SSH2 protocol library"

version = "2.7.1-m1"

requires = []

variants = [
    ["python-2.7"],
    ["python-3.7"],
]

pip_packages = [
    "paramiko==2.7.1",
]

private_build_requires = ["pipz"]
build_command = "install %s --bundle" % " ".join(pip_packages)


def commands():
    env = globals()["env"]

    env.PATH.prepend("{root}/bin")
    env.PYTHONPATH.prepend("{root}/python")
