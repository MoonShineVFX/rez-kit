
early = globals()["early"]


name = "python"

authors = ["Guido van Rossum"]

description = "The Python programming language"

version = "2.7.18-m1"

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
    alias = globals()["alias"]
    system = globals()["system"]

    if system.platform == "windows":
        env.PATH.prepend("{root}/payload")
        env.PATH.prepend("{root}/payload/Scripts")
    else:
        # untested
        env.PATH.prepend("{root}/payload/bin")

    # in case the entry points are still link to the original packaging
    # location. Or, pip install --upgrade to fix it.
    alias("pip", "python -m pip")
    alias("easy_install", "python -m easy_install")


uuid = "repository.python"
