
early = globals()["early"]  # lint helper


name = "Qt.py"

description = "Minimal Python 2 & 3 shim around all Qt bindings - " \
              "PySide, PySide2, PyQt4 and PyQt5."

version = "1.3.1"

requires = []


@early()
def variants():
    from rez import packages

    bindings = [
        "PyQt5",
        "PySide2",
        "PyQt4",
        "PySide",
    ]
    variants_ = [
        [binding] for binding in bindings
        if packages.get_latest_package_from_string(binding)
    ]
    if not variants_:
        raise Exception("No Qt binding package found.")

    return variants_


pip_packages = [
    "Qt.py==1.3.1",
]

private_build_requires = ["pipz"]
build_command = "install %s --bundle" % " ".join(pip_packages)


def commands():
    env = globals()["env"]

    env.PATH.prepend("{root}/bin")
    env.PYTHONPATH.prepend("{root}/python")
