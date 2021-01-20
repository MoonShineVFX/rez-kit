
name = "hou_mops"

version = "1.3-m1"

description = "See https://github.com/toadstorm/MOPS"

requires = [
    "houdini-17.5+<18.6",
]

private_build_requires = ["rezutil-1"]
build_command = "python {root}/rezbuild.py {install}"


def commands():
    env = globals()["env"]

    env.MOPS = "{root}/payload"
    env.HOUDINI_PATH.prepend("{root}/payload")
