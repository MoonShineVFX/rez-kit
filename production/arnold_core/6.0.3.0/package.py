
name = "arnold_core"

version = "6.0.3.0-m1"

build_command = False


def pre_commands():
    env = globals()["env"]

    env.ARNOLD_CORE_VERSION = \
        str(env.REZ_ARNOLD_CORE_VERSION).rsplit("-m", 1)[0]
