
name = "opensubdiv"

version = "3.4.3-m1"

variants = [
    ["arch-*", "os-*"],
]

build_requires = [
    "rezutil-1+",
    "cmake-3.2+",
    "zlib",
    "tbb",
    "ptex",
]
build_command = "python {root}/rezbuild.py {install}"


def commands():
    env = globals()["env"]

    env.PATH.append("{root}/bin")
    env.PATH.append("{root}/lib")
    env.LD_LIBRARY_PATH.append("{root}/lib")
    env.PKG_CONFIG_PATH.append("{root}/lib/pkgconfig")

    env.OPENSUBDIV_ROOT_DIR = "{root}"
    env.OPENSUBDIV_INCLUDE_DIR.append("{root}/include")
    env.OPENSUBDIV_LIBRARIES.append("{root}/lib")
