
name = "rezutil"

version = "1.4.5-m1"


# build with bez build system


def commands():
    env = globals()["env"]
    env.PYTHONPATH.prepend("{root}/python")
