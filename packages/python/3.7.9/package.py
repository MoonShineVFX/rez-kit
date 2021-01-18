
early = globals()["early"]


name = "python"

authors = ["Guido van Rossum"]

description = "The Python programming language"

version = "3.7.9-m1"

tools = [
    "python",
    "pythonw",
    "pip",
]

variants = [
    ["platform-*"],
]


private_build_requires = ["rezutil-1"]
build_command = "python {root}/rezbuild.py {install}"


def commands():
    env = globals()["env"]
    system = globals()["system"]

    if system.platform == "windows":
        env.PATH.prepend("{root}/payload")
        env.PATH.prepend("{root}/payload/Scripts")
    else:
        # untested
        env.PATH.prepend("{root}/payload/bin")


uuid = "repository.python"
