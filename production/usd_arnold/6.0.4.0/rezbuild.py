
import os
import sys
import platform
import subprocess
from rezutil import lib

PY3 = sys.version_info[0] == 3
IS_WIN = platform.system() == "Windows"
IS_LNX = platform.system() == "Linux"
IS_MAC = platform.system() == "Darwin"


url_prefix = "https://github.com/Autodesk/arnold-usd/archive"
filename = "arnold-6.0.4.0.zip"


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

    # Build
    arnold_root = os.environ["REZ_ARNOLD_SDK_ROOT"]
    usd_root = os.environ["REZ_USD_ROOT"]
    tbb_root = os.environ["REZ_TBB_ROOT"]
    boost_root = os.environ["REZ_BOOST_ROOT"]

    # For now assume Python was installed with rez scoopz which
    # installs the binaries into an `app` folder inside the root.
    python_root = os.path.join(os.environ["REZ_PYTHON_ROOT"], "payload")

    # Set build parameters
    args = [
        ("ARNOLD_PATH", arnold_root),
        ("USD_PATH", usd_root),
        # Set the build mode for USD that it generates when running
        # default build script, which is 'shared_libs'
        ("USD_BUILD_MODE", r"shared_libs"),
        ("USD_LIB_PREFIX", r""),
        # Set the BOOST_INCLUDE prefix for USD built on Windows using
        # Visual Studio 2017 or greater, which builds boost 1.65.1
        ("BOOST_INCLUDE", boost_root + "/include/boost-1_70"),
        # Building USD on Windows using Pixar's build script appends
        # a suffix to all Boost generated files, so we need to make
        # sure that Arnold-USD finds it.
        ("BOOST_LIB_NAME", "boost_%s-vc141-mt-1_70.lib"),
        ("PYTHON_INCLUDE", os.path.join(python_root, "include")),
        ("PYTHON_LIB", os.path.join(python_root, "libs")),
        ("PYTHON_LIB_NAME", r"python27"),
        ("TBB_INCLUDE", os.path.join(tbb_root, "include")),
        ("TBB_LIB", os.path.join(tbb_root, "lib")),
        ("BUILD_SCHEMAS", "True"),
        # todo: Fix building the docs. It fails on:
        # AttributeError: 'SConsEnvironment' object has no attribute 'Doxygen':
        #   File "D:\dev\usd\arnold-usd\SConstruct", line 392:
        #     DOCS = env.Doxygen(source='docs/Doxyfile', target=docs_output)
        ("BUILD_DOCS", "False"),
        ("DISABLE_CXX11_ABI", "True"),
        ("MSVC_VERSION", "14.1"),
        # Install location
        ("PREFIX", install_path)

    ]
    # todo: handle paths with spaces?
    cmd_build_args = ["%s=%s" % (key, value) for key, value in args]

    # Run arnold-usd/abuild
    cmd = [os.path.join(source_root, "abuild.bat")]
    cmd.extend(cmd_build_args)

    with lib.working_dir(source_root):
        subprocess.check_call(cmd)

        # Copy additional resources
        # copy_additionals(source_path, install_path)

        # Run test (Build will pass even test failed.)
        # env = os.environ.copy()
        # env["PATH"] += ";%s" % install_path + "/bin"
        # env["PATH"] += ";%s" % install_path + "/lib"
        # env["PATH"] += ";%s" % install_path + "/plugin/usd"
        # env["PYTHONPATH"] += ";%s" % install_path + "/lib/python"
        # # No need to set PYTHONHOME in production, just for testing
        # env["PYTHONHOME"] = os.environ["REZ_PYTHON_ROOT"] + "/payload"
        # subprocess.call([
        #     "ctest",
        #     "--output-on-failure",
        #     "--timeout", "300",
        #     "-C", "Debug" if is_debug else "Release",
        #     # "-R", "<single_test_name_here>",
        # ], env=env)


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
