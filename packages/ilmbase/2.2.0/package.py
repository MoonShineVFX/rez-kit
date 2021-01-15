
name = "ilmbase"

version = "2.2.0-m1"

variants = [
    ["arch", "os"],
]

build_requires = [
    "rezutil-1+",
    "cmake-3.12+",
]
build_command = "python {root}/rezbuild.py {install}"


def commands():
    env = globals()["env"]

    env.PATH.append("{root}/bin")
    env.PATH.append("{root}/lib")
    env.LD_LIBRARY_PATH.append("{root}/lib")
    env.PKG_CONFIG_PATH.append("{root}/lib/pkgconfig")

    env.ILMBASE_ROOT = "{root}"
