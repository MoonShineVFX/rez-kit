
import os
import sys
import platform
import subprocess
from rezutil import lib

PY3 = sys.version_info[0] == 3
IS_WIN = platform.system() == "Windows"
IS_LNX = platform.system() == "Linux"
IS_MAC = platform.system() == "Darwin"


url_prefix = "https://github.com/boostorg/build/archive"
filename = "4.3.0.tar.gz"


def build(source_path, build_path, install_path, targets):
    targets = targets or []
    if "install" not in targets:
        install_path = build_path + "/install"

    # Download the source
    url = "%s/%s" % (url_prefix, filename)
    archive = lib.download(url, filename)

    # Unzip the source
    dont_extract = ["*/doc/*", "*/libs/*/doc/*"]
    source_root = lib.open_archive(archive,
                                   dont_extract=dont_extract)

    # Bootstrap
    with lib.working_dir(source_root):
        bootstrap = "bootstrap.bat" if IS_WIN else "./bootstrap.sh"
        subprocess.check_call([bootstrap, "--prefix=%s" % install_path])

    # Build B2
    b2_exec = "b2" if IS_WIN else "./b2"
    b2_settings = [
        b2_exec,
        "install",
        "--prefix=%s" % install_path,
    ]

    # Build
    with lib.working_dir(source_root):
        subprocess.check_call(b2_settings)


if __name__ == "__main__":
    build(source_path=os.environ["REZ_BUILD_SOURCE_PATH"],
          build_path=os.environ["REZ_BUILD_PATH"],
          install_path=os.environ["REZ_BUILD_INSTALL_PATH"],
          targets=sys.argv[1:])
