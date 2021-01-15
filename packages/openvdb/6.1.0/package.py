
name = "openvdb"

version = "6.1.0-m1"

variants = [
    ["arch", "os"],
]

build_requires = [
    "rezutil-1+",
    "cmake-3.2+",
    "boost",
    "zlib",
    "blosc",
    "tbb",
    "openexr",  # for ilmbase
]
build_command = "python {root}/rezbuild.py {install}"


def commands():
    env = globals()["env"]

    env.PATH.append("{root}/bin")
    env.PATH.append("{root}/lib")
    env.LD_LIBRARY_PATH.append("{root}/lib")
    env.PKG_CONFIG_PATH.append("{root}/lib/pkgconfig")

    env.OPENVDB_ROOT = "{root}"
    env.OPENVDB_INCLUDE_DIR.append("{root}/include")
    env.OPENVDB_LIBRARY.append("{root}/lib")
