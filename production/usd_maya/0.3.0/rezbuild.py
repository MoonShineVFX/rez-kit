
import os
import sys
import platform
import subprocess
from rezutil import lib

PY3 = sys.version_info[0] == 3
IS_WIN = platform.system() == "Windows"
IS_LNX = platform.system() == "Linux"
IS_MAC = platform.system() == "Darwin"


url_prefix = "https://github.com/Autodesk/maya-usd/archive"
filename = "v0.3.0.zip"


def shorten_variant_build_path(source_path):
    """replace variant sub-path with index
    """
    variant = os.environ["REZ_BUILD_VARIANT_INDEX"]
    build_path = os.path.join(source_path, "build", variant)

    if not os.path.isdir(build_path):
        os.makedirs(build_path)
    os.chdir(build_path)

    return build_path


def build(source_path, build_path, install_path, targets):

    # Try to avoid too long path.
    build_path = shorten_variant_build_path(source_path)

    targets = targets or []
    if "install" not in targets:
        install_path = build_path + "/install"

    py_info = lib.python_info()
    is_debug = lib.is_debug_build()

    # Download the source
    url = "%s/%s" % (url_prefix, filename)
    archive = lib.download(url, filename)

    # Unzip the source
    source_root = lib.open_archive(archive)

    if is_debug:
        # For bypassing "fatal error LNK1104: cannot open 'python27_d.lib'"
        #
        # Although there's a flag `MAYAUSD_DEFINE_BOOST_DEBUG_PYTHON_FLAG`
        # for not using python debug, which will set `Boost_USE_DEBUG_PYTHON`
        # to `ON` when `MAYAUSD_DEFINE_BOOST_DEBUG_PYTHON_FLAG=ON`, but the
        # following settings still try to use python debug lib even it's OFF.
        #
        # Not sure what these patch will affect, but I *guess* it should be
        # safe..
        #
        cmake_lists = [
            "/lib/usd/utils/CMakeLists.txt",
            "/lib/usd/schemas/CMakeLists.txt",
            "/lib/mayaUsd/CMakeLists.txt",
            "/plugin/al/schemas/AL/usd/schemas/maya/CMakeLists.txt",
            "/plugin/al/schemas/AL/usd/schemas/mayatest/CMakeLists.txt",
            "/plugin/al/usdmayautils/AL/usdmaya/utils/CMakeLists.txt",
            "/plugin/al/usdtransaction/AL/usd/transaction/CMakeLists.txt",
            "/plugin/al/usdtransaction/AL/usd/transaction/tests/CMakeLists.txt",
        ]
        for fname in cmake_lists:
            lib.patch_file(
                source_root + fname,
                [("$<$<STREQUAL:${CMAKE_BUILD_TYPE},Debug>:BOOST_DEBUG_PYTHON>",
                  "# $<$<STREQUAL:${CMAKE_BUILD_TYPE},Debug>:BOOST_DEBUG_PYTHON>")]
            )

    # Build
    with lib.working_dir(build_path + "/_usd_maya"):
        extra_args = [
            "-DMAYAUSD_DEFINE_BOOST_DEBUG_PYTHON_FLAG=OFF",

            "-DBUILD_SHARED_LIBS=ON",
            "-DBUILD_WITH_PYTHON_3=OFF",
            "-DPython_EXECUTABLE=\"%s\"" % py_info[0].replace("\\", "/"),
            "-DPYTHON_LIBRARIES=\"%s\"" % py_info[1].replace("\\", "/"),
            "-DPYTHON_INCLUDE_DIRS=\"%s\"" % py_info[2].replace("\\", "/"),

            "-DBUILD_MAYAUSD_LIBRARY=ON",
            "-DBUILD_ADSK_PLUGIN=ON",
            "-DBUILD_PXR_PLUGIN=ON",
            "-DBUILD_AL_PLUGIN=ON",
            "-DBUILD_HDMAYA=ON",
            "-DCMAKE_WANT_UFE_BUILD=ON",

            "-DBUILD_TESTS=ON",
            "-DBUILD_STRICT_MODE=OFF",  # warning as error
            # If `BUILD_STRICT` enabled, may get encode warnings e.g. in
            #   `include\pxr/imaging/hd/renderIndex.h`, and build failed.

            "-DQT_LOCATION=\"%s\"" % os.environ["QT_LOCATION"],
        ]
        if IS_WIN:
            # Increase the precompiled header buffer limit.
            extra_args.append("-DCMAKE_CXX_FLAGS=\"/Zm150\"")

        lib.run_cmake(source_root, install_path, extra_args=extra_args)

        # Copy additional resources
        copy_additionals(source_path, install_path)

        # Run test (Build will pass even test failed.)
        os.environ["MAYA_MODULE_PATH"] = "%s" % install_path
        os.environ["PYTHONPATH"] += ";%s" % os.environ["REZ_FUTURE_ROOT"]
        subprocess.call([
            "ctest",
            "--output-on-failure",
            "--timeout", "300",
            "-C", "Debug" if is_debug else "Release",
            # "-R", "<single_test_name_here>",
        ])


def copy_additionals(source_path, install_path):
    for dirname in ["resources"]:
        src = os.path.join(source_path, dirname)
        dst = os.path.join(install_path, dirname)
        lib.copy_dir(src, dst)


if __name__ == "__main__":
    build(source_path=os.environ["REZ_BUILD_SOURCE_PATH"],
          build_path=os.environ["REZ_BUILD_PATH"],
          install_path=os.environ["REZ_BUILD_INSTALL_PATH"],
          targets=sys.argv[1:])
