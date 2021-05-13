
import os
import sys
import platform
from rezutil import lib

IS_WIN = platform.system() == "Windows"


url_prefix = "https://github.com/alembic/alembic/archive"
filename = "1.7.1.zip"


def build(source_path, build_path, install_path, targets):
    targets = targets or []
    if "install" not in targets:
        install_path = build_path + "/install"

    # Download the source
    url = "%s/%s" % (url_prefix, filename)
    archive = lib.download(url, filename)

    # Unzip the source
    source_root = lib.open_archive(archive)

    # Patch
    if IS_WIN:
        # Alembic doesn't link against HDF5 libraries on Windows
        # whether or not USE_HDF5=ON or not.  There is a line to link
        # against HDF5 on DARWIN so we hijack it to also link on WIN32.
        lib.patch_file(
            source_root + "/lib/Alembic/CMakeLists.txt",
            [("ALEMBIC_SHARED_LIBS AND DARWIN",
              "ALEMBIC_SHARED_LIBS AND DARWIN OR ALEMBIC_SHARED_LIBS AND WIN32")]
        )

    # Build
    with lib.working_dir(build_path + "/_alembic"):
        extra_args = [
            "-DUSE_BINARIES=OFF",
            "-DUSE_TESTS=OFF",
            # hdf5
            "-DUSE_HDF5=ON",
            "-DHDF5_ROOT=\"%s\"" % os.getenv("REZ_HDF5_ROOT", install_path),
            "-DCMAKE_CXX_FLAGS=\"-D H5_BUILT_AS_DYNAMIC_LIB\""
        ]
        lib.run_cmake(source_root, install_path, extra_args=extra_args)


if __name__ == "__main__":
    build(source_path=os.environ["REZ_BUILD_SOURCE_PATH"],
          build_path=os.environ["REZ_BUILD_PATH"],
          install_path=os.environ["REZ_BUILD_INSTALL_PATH"],
          targets=sys.argv[1:])
