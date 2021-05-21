
name = "rezutil"

version = "1.4.6-m2"

build_command = "python {root}/rezbuild.py {install}"


def commands():
    env = globals()["env"]
    building = globals()["building"]

    env.PYTHONPATH.prepend("{root}/python")
    if building:
        # PYTHONPATH will be ignored in production installed rez
        env.REZ_PACKAGE_DEFINITION_BUILD_PYTHON_PATHS.prepend("{root}/python")
