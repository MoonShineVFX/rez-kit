
import os
import sys
from rezutil import lib


url_prefix = "https://sourceforge.net/projects/libpng/files/libpng16/older-releases/1.6.29"
filename = "libpng-1.6.29.tar.gz"


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
    with lib.working_dir(build_path + "/_libpng"):
        lib.run_cmake(source_root, install_path, build_type="Debug")
        lib.run_cmake(source_root, install_path, build_type="Release")


if __name__ == "__main__":
    build(source_path=os.environ["REZ_BUILD_SOURCE_PATH"],
          build_path=os.environ["REZ_BUILD_PATH"],
          install_path=os.environ["REZ_BUILD_INSTALL_PATH"],
          targets=sys.argv[1:])
