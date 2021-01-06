
name = "b2"

version = "4.3.0-m1"

description = "Boost build tool."

variants = [
    ["arch-*", "os-*"],
]

tools = [
    "b2",
]

build_requires = [
    "rezutil-1+",
    "rez",
]
build_command = "python {root}/rezbuild.py {install}"


def commands():
    env = globals()["env"]

    env.PATH.prepend("{root}/bin")
