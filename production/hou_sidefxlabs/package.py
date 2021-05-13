
name = "hou_sidefxlabs"

version = "18.5.447-m1"

description = "See https://github.com/sideeffects/SideFXLabs "\
              "and https://www.sidefx.com/products/sidefx-labs/"

requires = [
    "houdini-18.0+<18.6",
]

private_build_requires = ["rezutil-1"]
build_command = "python {root}/rezbuild.py {install}"


def commands():
    env = globals()["env"]

    env.SIDEFXLABS = "{root}/payload"
    env.PATH.prepend("{root}/payload/bin")
    env.HOUDINI_PATH.prepend("{root}/payload")
