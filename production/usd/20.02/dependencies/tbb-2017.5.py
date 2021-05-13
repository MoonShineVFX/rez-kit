
import os
import sys
import platform
import subprocess
from rezutil import lib

IS_WIN = platform.system() == "Windows"
IS_LNX = platform.system() == "Linux"
IS_MAC = platform.system() == "Darwin"


if IS_WIN:
    url_prefix = "https://github.com/oneapi-src/oneTBB/releases/download/2017_U5"
    filename = "tbb2017_20170226oss_win.zip"
else:
    url_prefix = "https://github.com/oneapi-src/oneTBB/archive"
    filename = "4.4.6.tar.gz"


def build(source_path, build_path, install_path, targets):
    targets = targets or []
    if "install" not in targets:
        install_path = build_path + "/install"

    # Download the source
    url = "%s/%s" % (url_prefix, filename)
    archive = lib.download(url, filename)

    # Unzip the source
    source_root = lib.open_archive(archive)

    # build
    if IS_WIN:
        win_build(source_root, install_path)
    else:
        lnx_mac_build(source_root, install_path)


def win_build(source, install):
    # On Windows, we simply copy headers and pre-built DLLs to
    # the appropriate location.
    # Install the files, like usd build script:
    lib.copy_files(source + "/bin/intel64/vc14/*.*", install + "/bin")
    lib.copy_files(source + "/lib/intel64/vc14/*.*", install + "/lib")
    lib.copy_dir(source + "/include/tbb", install + "/include/tbb")
    lib.copy_dir(source + "/include/serial", install + "/include/serial")


def lnx_mac_build(source, install):
    if IS_MAC:
        # Note: TBB installation fails on OSX when cuda is installed, a
        # suggested fix:
        # https://github.com/spack/spack/issues/6000#issuecomment-358817701
        lib.patch_file(
            source + "/build/macos.inc",
            [("shell clang -v ", "shell clang --version ")]
        )

    # TBB does not support out-of-source builds in a custom location.
    args = [
        "make",
        "-j%s" % os.environ["REZ_BUILD_THREAD_COUNT"],
    ]
    subprocess.check_call(args, cwd=source)

    # Install both release and debug builds. USD requires the debug
    # libraries when building in debug mode, and installing both
    # makes it easier for users to install dependencies in some
    # location that can be shared by both release and debug USD
    # builds. Plus, the TBB build system builds both versions anyway.
    lib.copy_files(source + "/build/*_release/libtbb*.*", install + "/bin")
    lib.copy_files(source + "/build/*_debug/libtbb*.*", install + "/lib")
    lib.copy_dir(source + "/include/tbb", install + "/include/tbb")
    lib.copy_dir(source + "/include/serial", install + "/include/serial")


if __name__ == "__main__":
    build(source_path=os.environ["REZ_BUILD_SOURCE_PATH"],
          build_path=os.environ["REZ_BUILD_PATH"],
          install_path=os.environ["REZ_BUILD_INSTALL_PATH"],
          targets=sys.argv[1:])
