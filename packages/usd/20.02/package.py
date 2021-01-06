
name = "usd"

version = "20.02"

_data = {
    # Allzpark
    "label": "USD",
    "icon": "{root}/resources/usd.png"
}

requires = [
    "python",
    "PyOpenGL",
    "PySide",
]

variants = [
    ["platform-*", "python-2.7", "release-1"],
    ["platform-*", "python-2.7", "release-0"],
]


build_requires = [
    "rezutil-1+",
    "cmake-3.2+",
    "doxygen",
    "graphviz",
    "nasm",
    "jinja2",
]
dependencies = [
    "zlib-1.2.11",
    "boost-1.65.1",
    "tbb-2017.5",
    "glew-2.0.0",
    "libpng-1.6.29",
    "libjpeg_turbo-1.5.1",
    "libtiff-4.0.7",
    "ptex-2.1.28",
    "hdf5-1.10.0",
    "blosc-1.17.0",
    "openexr-2.2.0",
    "opensubdiv-3.1.1",
    "openvdb-6.1.0",
    "opencolorio-1.1.0",
    "openimageio-1.7.14",
    "alembic-1.7.1",
    "materialx-1.36.0",
]
private_build_requires = [
    # "rez",  # for building boost
    "nuke-11+",  # for openimageio
]
build_command = "\n".join([
    "python {root}/dependencies/%s.py {install}" % dep
    for dep in dependencies
] + [
    "python {root}/rezbuild.py {install}",
    "cd ."  # This will make the build process always success !
])


def pre_build_commands():
    import os
    build = globals()["build"]
    os.environ["PATH"] += ";%s;%s" % (build.install_path + "/bin",
                                      build.install_path + "/lib")


def commands():
    env = globals()["env"]
    system = globals()["system"]

    env.PATH.append("{root}/bin")
    env.PATH.append("{root}/plugin/usd")
    env.PYTHONPATH.append("{root}/lib/python")

    if system.platform == "windows":
        # Required additionally on Windows
        env.PATH.append("{root}/lib")

    elif system.platform == "linux":
        env.LD_LIBRARY_PATH.append("{root}/lib")

    env.PXR_USD_LOCATION = "{root}"
