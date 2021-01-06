"""
This rez build script was based on:
https://github.com/PixarAnimationStudios/USD/blob/v20.08/build_scripts/build_usd.py
"""
import os
import sys
import platform
import subprocess
from rezutil import lib

PY3 = sys.version_info[0] == 3
IS_WIN = platform.system() == "Windows"
IS_LNX = platform.system() == "Linux"
IS_MAC = platform.system() == "Darwin"


url_prefix = "https://github.com/PixarAnimationStudios/USD/archive"
filename = "v20.08.zip"


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

    # We need to shorten build path if DPXR_BUILD_EXAMPLES is ON.
    # This is not perfect, but it is suffice for now.
    build_path = shorten_variant_build_path(source_path)

    rebuild = True

    targets = targets or []
    if "install" not in targets:
        install_path = build_path + "/install"

    is_debug = lib.is_debug_build()
    py_info = lib.python_info()

    # Clean build
    if rebuild:
        lib.clear_build(build_path)

    # Download the source
    archive = os.path.join(build_path, filename)
    if rebuild:
        url = "%s/%s" % (url_prefix, filename)
        lib.download(url, archive)

    # Unzip the source
    source_root = lib.open_archive(archive, cleanup=rebuild)

    # Patch
    # Fix "openvdb\Types.h(36):
    #   fatal error C1083: cannot open file: 'OpenEXR/half.h' ..."
    lib.patch_file(
        source_root + "/pxr/imaging/glf/CMakeLists.txt",
        [("list(APPEND optionalIncludeDirs ${OPENVDB_INCLUDE_DIR})",
          "list(APPEND optionalIncludeDirs ${OPENVDB_INCLUDE_DIR} ${OPENEXR_INCLUDE_DIR})")]
    )
    # Fix finding usd tools exec on Windows
    lib.patch_file(
        source_root + "/pxr/usd/bin/usddiff/usddiff.py",
        [(_usddiff_code_a + _win_code, _usdtools_patch)],
        multiline_matches=True
    )
    lib.patch_file(
        source_root + "/pxr/usd/bin/usdedit/usdedit.py",
        [(_usdedit_code_a + _win_code, _usdtools_patch)],
        multiline_matches=True
    )

    # Build
    with lib.working_dir(build_path + "/_usd"):
        extra_args = [
            "-DTBB_USE_DEBUG_BUILD=" + "ON" if is_debug else "OFF",

            "-DPXR_ENABLE_PYTHON_SUPPORT=ON",
            "-DPXR_USE_PYTHON_3=%s" % "ON" if PY3 else "OFF",
            "-DPYTHON_EXECUTABLE=\"%s\"" % py_info[0],
            "-DPYTHON_LIBRARY=\"%s\"" % py_info[1],
            "-DPYTHON_INCLUDE_DIR=\"%s\"" % py_info[2],

            "-DBUILD_SHARED_LIBS=ON",
            "-DPXR_BUILD_DOCUMENTATION=ON",
            "-DPXR_BUILD_EXAMPLES=ON",
            "-DPXR_BUILD_TESTS=ON",
            "-DPXR_BUILD_TUTORIALS=ON",
            "-DPXR_BUILD_USD_TOOLS=ON",
            "-DPXR_BUILD_USDVIEW=ON",

            # boost
            "-DBoost_NO_BOOST_CMAKE=On",
            "-DBoost_NO_SYSTEM_PATHS=True",
            "-DBOOST_ROOT=\"%s\"" % os.getenv("BOOST_ROOT", install_path),

            "-DPXR_BUILD_IMAGING=ON",
            "-DPXR_BUILD_USD_IMAGING=ON",
            "-DPXR_ENABLE_PTEX_SUPPORT=ON",
            "-DPXR_ENABLE_OPENVDB_SUPPORT=ON",
            "-DPXR_BUILD_OPENIMAGEIO_PLUGIN=ON",
            "-DPXR_BUILD_OPENCOLORIO_PLUGIN=ON",
            "-DPXR_BUILD_MATERIALX_PLUGIN=ON",

            "-DPXR_BUILD_ALEMBIC_PLUGIN=ON",
            "-DPXR_ENABLE_HDF5_SUPPORT=ON",
            "-DHDF5_ROOT=\"%s\"" % os.getenv("REZ_HDF5_ROOT", install_path),
            "-DALEMBIC_DIR=\"%s\"" % os.getenv("REZ_ALEMBIC_ROOT", install_path),
            "-DGLEW_LOCATION=\"%s\"" % os.getenv("REZ_GLEW_ROOT", install_path),

            "-DPXR_BUILD_EMBREE_PLUGIN=OFF",
            "-DPXR_BUILD_PRMAN_PLUGIN=OFF",
            "-DPXR_BUILD_DRACO_PLUGIN=OFF",

            # PXR_VALIDATE_GENERATED_CODE
            # hgiMetal
            # PXR_BUILD_GPU_SUPPORT
            # PXR_ENABLE_METAL_SUPPORT
        ]
        if IS_WIN:
            # Increase the precompiled header buffer limit.
            extra_args.append("-DCMAKE_CXX_FLAGS=\"/Zm150\"")

        lib.run_cmake(source_root, install_path, extra_args=extra_args)

        # Copy additional resources
        copy_additionals(source_path, install_path)

        # Run test (Build will pass even test failed.)
        env = os.environ.copy()
        required_path = os.pathsep.join(
            install_path + dirname for dirname in
            ["/bin", "/lib", "/plugin/usd"]
        )  # must be prepended.
        env["PATH"] = os.pathsep.join([required_path, env["PATH"]])
        env["PYTHONPATH"] += ";%s" % install_path + "/lib/python"
        # No need to set PYTHONHOME in production, just for testing
        env["PYTHONHOME"] = os.environ["REZ_PYTHON_ROOT"] + "/payload"
        subprocess.call([
            "ctest",
            "--output-on-failure",
            "--timeout", "300",
            "-C", "Debug" if is_debug else "Release",
            # "-R", "<single_test_name_here>",
        ], env=env)


def copy_additionals(source_path, install_path):
    for dirname in ["resources"]:
        src = os.path.join(source_path, dirname)
        dst = os.path.join(install_path, dirname)
        lib.copy_dir(src, dst)


_usddiff_code_a = """def _findExe(name):
    from distutils.spawn import find_executable
    cmd = find_executable(name)
    
    if cmd:
        return cmd
    else:
        cmd = find_executable(name, path=os.path.abspath(os.path.dirname(sys.argv[0])))
        if cmd:
            return cmd

"""
_usdedit_code_a = """def _findExe(name):
    from distutils.spawn import find_executable
    cmd = find_executable(name)
    if cmd:
        return cmd
    else:
        cmd = find_executable(name, path=os.path.abspath(os.path.dirname(sys.argv[0])))
        if cmd:
            return cmd
    
"""
_win_code = """    if isWindows:
        # find_executable under Windows only returns *.EXE files
        # so we need to traverse PATH.
        for path in os.environ['PATH'].split(os.pathsep):
            base = os.path.join(path, name)
            # We need to test for name.cmd first because on Windows, the USD
            # executables are wrapped due to lack of N*IX style shebang support
            # on Windows.
            for ext in ['.cmd', '']:
                cmd = base + ext
                if os.access(cmd, os.X_OK):
                    return cmd
    return None
"""

_usdtools_patch = """def __findExe(name):
    from distutils.spawn import find_executable
    cmd = find_executable(name)
    if cmd:
        return cmd
    else:
        cmd = find_executable(name, path=os.path.abspath(os.path.dirname(sys.argv[0])))
        if cmd:
            return cmd
    return None

def __findExe_Win(name):
    cmd = __findExe(name)
    if cmd and os.access(cmd + '.cmd', os.X_OK):
        return cmd + '.cmd'

    # find_executable under Windows only returns *.EXE files (Python 3.7+)
    # so we need to traverse PATH.
    for path in os.environ['PATH'].split(os.pathsep):
        base = os.path.join(path, name)
        # We need to test for name.cmd first because on Windows, the USD
        # executables are wrapped due to lack of N*IX style shebang support
        # on Windows.
        for ext in ['.cmd', '']:
            cmd = base + ext
            if os.access(cmd, os.X_OK):
                return cmd
    return None

if isWindows:
    _findExe = __findExe_Win
else:
    _findExe = __findExe
"""


if __name__ == "__main__":
    build(source_path=os.environ["REZ_BUILD_SOURCE_PATH"],
          build_path=os.environ["REZ_BUILD_PATH"],
          install_path=os.environ["REZ_BUILD_INSTALL_PATH"],
          targets=sys.argv[1:])
