
name = "jinja2"

description = "A very fast and expressive template engine."

version = "2.11.2-m1"

requires = []

variants = [
    ["python-2.7"],
    ["python-3.7"],
]

pip_packages = [
    "jinja2==2.11.2",
]

private_build_requires = ["pipz"]
build_command = "install %s --bundle" % " ".join(pip_packages)


def commands():
    env = globals()["env"]

    env.PATH.prepend("{root}/bin")
    env.PYTHONPATH.prepend("{root}/python")
