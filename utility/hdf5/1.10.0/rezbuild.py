
import os
import sys
from rezutil import lib


url_prefix = "https://support.hdfgroup.org/ftp/HDF5/releases/hdf5-1.10/hdf5-1.10.0-patch1/src"
filename = "hdf5-1.10.0-patch1.zip"


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
    with lib.working_dir(build_path + "/_hdf5"):
        extra_args = [
            "-DBUILD_TESTING=OFF",
            "-DHDF5_BUILD_TOOLS=OFF",
            "-DHDF5_BUILD_EXAMPLES=OFF",
        ]
        lib.run_cmake(source_root, install_path, extra_args=extra_args,
                      build_type="Debug")
        lib.run_cmake(source_root, install_path, extra_args=extra_args,
                      build_type="Release")


if __name__ == "__main__":
    build(source_path=os.environ["REZ_BUILD_SOURCE_PATH"],
          build_path=os.environ["REZ_BUILD_PATH"],
          install_path=os.environ["REZ_BUILD_INSTALL_PATH"],
          targets=sys.argv[1:])
