
name = "libtiff"

version = "4.0.7-m1"

variants = [
    ["arch", "os"],
]

build_requires = [
    "rezutil-1+",
    "cmake-3.2+",
    "zlib",
    "libjpeg_turbo",
]
build_command = "python {root}/rezbuild.py {install}"


def commands():
    env = globals()["env"]

    env.PATH.append("{root}/bin")
    env.PATH.append("{root}/lib")
    env.LD_LIBRARY_PATH.append("{root}/lib")
    env.PKG_CONFIG_PATH.append("{root}/lib/pkgconfig")

    env.TIFF_ROOT = "{root}"
    env.TIFF_INCLUDE_DIR.append("{root}/include")
    env.TIFF_LIBRARY.append("{root}/lib")
