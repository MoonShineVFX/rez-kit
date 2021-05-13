
name = "hou_qlib"

version = "0.2.187-m1"

description = "See https://github.com/qLab/qLib"

requires = [
    "houdini-17.5.321+<18.6",
]

private_build_requires = ["rezutil-1"]
build_command = "python {root}/rezbuild.py {install}"


def commands():
    env = globals()["env"]

    env.QLIB = "{root}/payload"
    env.QOTL = "{root}/payload/otls"
    env.HOUDINI_OTLSCAN_PATH.prepend("{root}/payload/otls/experimental")
    env.HOUDINI_OTLSCAN_PATH.prepend("{root}/payload/otls/future")
    env.HOUDINI_OTLSCAN_PATH.prepend("{root}/payload/otls/base")
    env.HOUDINI_PATH.prepend("{root}/payload")
