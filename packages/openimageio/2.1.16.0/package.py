
name = "openimageio"

version = "2.1.16.0-m1"

variants = [
    ["arch", "os"],
]

build_requires = [
    "rezutil-1+",
    "cmake-3.12+",
    "boost",
    "tbb",
    "libjpeg_turbo",
    "libpng",
    "libtiff",
    "ptex",
    "hdf5",
    "openexr-2.0+",
    "openvdb-5.0+",
    "opencolorio-1.1+",

    "nuke-11",

    # "qt-5.6+",
    # "opengl",
]
build_command = "python {root}/rezbuild.py {install}"


def commands():
    env = globals()["env"]

    env.PATH.append("{root}/bin")
    env.PATH.append("{root}/lib")
    env.LD_LIBRARY_PATH.append("{root}/lib")
    env.PKG_CONFIG_PATH.append("{root}/lib/pkgconfig")

    env.OPENIMAGEIO_ROOT = "{root}"
    env.OPENIMAGEIO_INCLUDE_DIR.append("{root}/include")
    env.OPENIMAGEIO_LIBRARY.append("{root}/lib")
