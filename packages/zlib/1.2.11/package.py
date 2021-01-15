
name = "zlib"

version = "1.2.11-m1"

variants = [
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
    env.PKG_CONFIG_PATH.append("{root}/share/pkgconfig")

    env.ZLIB_ROOT.set("{root}")
    env.ZLIB_INCLUDE_DIR.append("{root}/include")
    env.ZLIB_LIBRARY.append("{root}/lib")
