
import os
import sys
from rezutil import lib


url_prefix = "https://github.com/imageworks/OpenColorIO/archive"
filename = "v1.1.0.zip"


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
    with lib.working_dir(build_path + "/_opencolorio"):
        extra_args = [
            "-DOCIO_BUILD_TRUELIGHT=OFF",
            "-DOCIO_BUILD_APPS=OFF",
            "-DOCIO_BUILD_NUKE=OFF",
            "-DOCIO_BUILD_DOCS=OFF",
            "-DOCIO_BUILD_TESTS=OFF",
            "-DOCIO_BUILD_PYGLUE=OFF",
            "-DOCIO_BUILD_JNIGLUE=OFF",
            "-DOCIO_STATIC_JNIGLUE=OFF",
        ]
        lib.run_cmake(source_root, install_path, extra_args=extra_args)


if __name__ == "__main__":
    build(source_path=os.environ["REZ_BUILD_SOURCE_PATH"],
          build_path=os.environ["REZ_BUILD_PATH"],
          install_path=os.environ["REZ_BUILD_INSTALL_PATH"],
          targets=sys.argv[1:])
