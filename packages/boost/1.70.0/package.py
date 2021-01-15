
name = "boost"

version = "1.70.0-m1"

description = \
    """
    Boost provides free peer-reviewed portable C++ source libraries.
    """

variants = [
    ["arch", "os"],
]

build_requires = [
    "rezutil-1+",
    "rez",
]
build_command = "python {root}/rezbuild.py {install}"


def commands():
    env = globals()["env"]

    env.PATH.prepend("{root}/lib")
    env.LD_LIBRARY_PATH.prepend("{root}/lib")

    env.BOOST_ROOT = "{root}"
