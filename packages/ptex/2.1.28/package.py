
name = "ptex"

version = "2.1.28"

variants = [
    ["arch-*", "os-*", "release-1"],
    ["arch-*", "os-*", "release-0"],
]

build_requires = [
    "rezutil-1+",
    "cmake-3.2+",
    "zlib",
]
build_command = "python {root}/rezbuild.py {install}"


def commands():
    env = globals()["env"]

    env.PATH.append("{root}/bin")
    env.PATH.append("{root}/lib")
    env.LD_LIBRARY_PATH.append("{root}/lib")
    env.PKG_CONFIG_PATH.append("{root}/lib/pkgconfig")

    env.PTEX_ROOT = "{root}"
    env.PTEX_INCLUDE_DIR.append("{root}/include")
    env.PTEX_LIBRARY.append("{root}/lib")
