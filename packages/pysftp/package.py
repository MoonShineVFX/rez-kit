
name = "pysftp"

description = "A friendly face on SFTP"

version = "0.2.9-m1"

requires = []

variants = [
    ["python-2.7"],
    ["python-3.7"],
]

pip_packages = [
    "pysftp==0.2.9",
]

private_build_requires = ["pipz"]
build_command = "install %s --bundle" % " ".join(pip_packages)


def commands():
    env = globals()["env"]

    env.PATH.prepend("{root}/bin")
    env.PYTHONPATH.prepend("{root}/python")
