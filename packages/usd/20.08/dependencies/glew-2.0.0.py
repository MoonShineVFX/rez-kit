
import os
import sys
import platform
import subprocess
from rezutil import lib

IS_WIN = platform.system() == "Windows"


if IS_WIN:
    url_prefix = "https://sourceforge.net/projects/glew/files/glew/2.0.0"
    filename = "glew-2.0.0-win32.zip"
else:
    url_prefix = "https://sourceforge.net/projects/glew/files/glew/2.0.0"
    filename = "glew-2.0.0.tgz"


def build(source_path, build_path, install_path, targets):
    targets = targets or []
    if "install" not in targets:
        install_path = build_path + "/install"

    # Download the source
    url = "%s/%s" % (url_prefix, filename)
    archive = lib.download(url, filename)

    # Unzip the source
    source_root = lib.open_archive(archive)

    # Build
    if IS_WIN:
        win_build(source_root, install_path)
    else:
        lnx_mac_build(source_root, install_path)


def win_build(source, install):
    # On Windows, we install headers and pre-built binaries per
    # https://glew.sourceforge.net/install.html
    # Note that we are installing just the shared library. This is required
    # by the USD build; if the static library is present, that one will be
    # used and that causes errors with USD and OpenSubdiv.
    lib.copy_files(source + "/bin/Release/x64/glew32.dll", install + "/bin")
    lib.copy_files(source + "/lib/Release/x64/glew32.lib", install + "/lib")
    lib.copy_dir(source + "/include/GL", install + "/include/GL")


def lnx_mac_build(source, install):
    args = [
        "make",
        "GLEW_DEST=" + install,
        "-j%s" % os.environ["REZ_BUILD_THREAD_COUNT"],
        "install"
    ]
    subprocess.check_call(args, cwd=source)


if __name__ == "__main__":
    build(source_path=os.environ["REZ_BUILD_SOURCE_PATH"],
          build_path=os.environ["REZ_BUILD_PATH"],
          install_path=os.environ["REZ_BUILD_INSTALL_PATH"],
          targets=sys.argv[1:])
