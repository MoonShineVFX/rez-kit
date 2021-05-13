
name = "rich"

description = "Render rich text, tables, progress bars, " \
              "syntax highlighting, markdown and more to the terminal"

version = "6.0.0-m1"

requires = []

variants = [
    ["python-3.7"],
]

pip_packages = [
    "rich==6.0.0",
]

private_build_requires = ["pipz"]
build_command = "install %s --bundle" % " ".join(pip_packages)


def commands():
    env = globals()["env"]

    env.PATH.prepend("{root}/bin")
    env.PYTHONPATH.prepend("{root}/python")
