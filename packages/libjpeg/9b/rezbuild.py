
import os
import sys
import platform
import subprocess
from rezutil import lib

IS_WIN = platform.system() == "Windows"


url_prefix = "https://www.ijg.org/files"
if IS_WIN:
    filename = "jpegsrc9b.zip"
else:
    filename = "jpegsrc.v9b.tar.gz"


def build(source_path, build_path, install_path, targets):
    targets = targets or []
    if "install" not in targets:
        install_path = build_path + "/install"

    # Download the source
    url = "%s/%s" % (url_prefix, filename)
    archive = lib.download(url, filename)

    # Unzip the source
    source_root = lib.open_archive(archive)

    # Build libjpeg
    with lib.working_dir(source_root):
        args = [
            "./configure",
            "--prefix=" + install_path,
            "--disable-static",
            "--enable-shared",
        ]
        subprocess.check_call(args)

        args = [
            "make",
            "-j%s" % os.environ["REZ_BUILD_THREAD_COUNT"],
            "install",
        ]
        subprocess.check_call(args)


if __name__ == "__main__":
    build(source_path=os.environ["REZ_BUILD_SOURCE_PATH"],
          build_path=os.environ["REZ_BUILD_PATH"],
          install_path=os.environ["REZ_BUILD_INSTALL_PATH"],
          targets=sys.argv[1:])
