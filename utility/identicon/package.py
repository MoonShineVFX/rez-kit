

name = "identicon"

version = "1.0.0-m1"

authors = [
    "Usman Mahmood",
    "davidlatwe",
]

github = "https://github.com/davidlatwe/identicon"

description = (
    "Identicon is a python 3 script which generates "
    "Github like identicons (the default avatar you "
    "get when you sign up for a Github account)."
)

requires = [
    "python",
    "Pillow",
]

build_command = "python {root}/rezbuild.py {install}"


def commands():
    env = globals()["env"]

    env.PATH.prepend("{root}/bin")
    env.PYTHONPATH.prepend("{root}/python")
