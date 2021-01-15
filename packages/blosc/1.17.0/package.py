
name = "blosc"

version = "1.17.0-m1"

variants = [
    ["arch", "os"],
    ["arch", "os"],
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
    env.LD_LIBRARY_PATH.append("{root}/lib")
    env.PKG_CONFIG_PATH.append("{root}/lib/pkgconfig")

    env.BLOSC_ROOT = "{root}"
    env.BLOSC_INCLUDE_DIR.append("{root}/include")
    env.BLOSC_LIBRARY.append("{root}/lib")
