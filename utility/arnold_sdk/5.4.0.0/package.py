
name = "arnold_sdk"

version = "5.4.0.0-m1"

requires = [
    "arnold_core-%s" % version,
]

variants = [
    ["platform-*"]
]

private_build_requires = ["rezutil-1"]
build_command = "python -m rezutil build {root} --use-zip"


def commands():
    env = globals()["env"]

    env.ARNOLD_LOCATION = "{root}"
