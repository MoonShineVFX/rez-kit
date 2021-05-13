
import os
import sys
from rezutil import lib


url_prefix = "https://download.osgeo.org/libtiff"
filename = "tiff-4.0.7.zip"


def build(source_path, build_path, install_path, targets):
    targets = targets or []
    if "install" not in targets:
        install_path = build_path + "/install"

    # Download the source
    url = "%s/%s" % (url_prefix, filename)
    archive = lib.download(url, filename)

    # Unzip the source
    source_root = lib.open_archive(archive)

    # libTIFF has a build issue on Windows where tools/tiffgt.c
    # unconditionally includes unistd.h, which does not exist.
    # To avoid this, we patch the CMakeLists.txt to skip building
    # the tools entirely. We do this on Linux and MacOS as well
    # to avoid requiring some GL and X dependencies.
    #
    # We also need to skip building tests, since they rely on
    # the tools we've just elided.
    lib.patch_file(
        source_root + "/CMakeLists.txt",
        [("add_subdirectory(tools)", "# add_subdirectory(tools)"),
         ("add_subdirectory(test)", "# add_subdirectory(test)")]
    )

    # Build
    with lib.working_dir(build_path + "/_libtiff"):
        lib.run_cmake(source_root, install_path, build_type="Debug")
        lib.run_cmake(source_root, install_path, build_type="Release")


if __name__ == "__main__":
    build(source_path=os.environ["REZ_BUILD_SOURCE_PATH"],
          build_path=os.environ["REZ_BUILD_PATH"],
          install_path=os.environ["REZ_BUILD_INSTALL_PATH"],
          targets=sys.argv[1:])
