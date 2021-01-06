
early = globals()["early"]  # lint helper


name = "Qt5.py"

description = "Minimal Python 2 & 3 shim around PySide2 and PyQt5."

version = "0.2.0.b2-m1"

requires = []


@early()
def variants():
    from rez import packages

    bindings = [
        "PyQt5",
        "PySide2",
    ]
    variants_ = [
        [binding] for binding in bindings
        if packages.get_latest_package_from_string(binding)
    ]
    if not variants_:
        raise Exception("No Qt binding package found.")

    return variants_


pip_packages = [
    "Qt5.py==0.2.0.b2",
]

private_build_requires = ["pipz"]
build_command = "install %s --bundle" % " ".join(pip_packages)


def commands():
    env = globals()["env"]

    env.PATH.prepend("{root}/bin")
    env.PYTHONPATH.prepend("{root}/python")
