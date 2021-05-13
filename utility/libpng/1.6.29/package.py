
name = "libpng"

version = "1.6.29-m1"

requires = [
    "zlib",
]

variants = [
    ["arch-*", "os-*"],
]

build_requires = [
    "rezutil-1+",
    "cmake-3.2+",
]
build_command = "python {root}/rezbuild.py {install}"


def commands():
    env = globals()["env"]

    env.PATH.append("{root}/bin")
    env.PATH.append("{root}/lib")
