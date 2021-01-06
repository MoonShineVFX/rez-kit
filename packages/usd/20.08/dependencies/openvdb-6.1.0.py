
import os
import sys
from rezutil import lib


url_prefix = "https://github.com/AcademySoftwareFoundation/openvdb/archive"
filename = "v6.1.0.zip"


def build(source_path, build_path, install_path, targets):
    targets = targets or []
    if "install" not in targets:
        install_path = build_path + "/install"

    is_debug = lib.is_debug_build()

    # Download the source
    url = "%s/%s" % (url_prefix, filename)
    archive = lib.download(url, filename)

    # Unzip the source
    source_root = lib.open_archive(archive)

    if is_debug:
        lib.patch_file(
            source_root + "/cmake/FindTBB.cmake",
            [("find_library(Tbb_${COMPONENT}_LIBRARY ${COMPONENT}",
              "find_library(Tbb_${COMPONENT}_LIBRARY ${COMPONENT}_debug")]
        )

    # Build
    with lib.working_dir(build_path + "/_openvdb"):
        extra_args = [
            "-DOPENVDB_BUILD_PYTHON_MODULE=OFF",
            "-DOPENVDB_BUILD_BINARIES=OFF",
            "-DOPENVDB_BUILD_UNITTESTS=OFF",

            # boost
            "-DBoost_NO_BOOST_CMAKE=On",
            "-DBoost_NO_SYSTEM_PATHS=True",
            "-DBOOST_ROOT=\"%s\"" % os.getenv("BOOST_ROOT", install_path),
            # blosc
            "-DBLOSC_ROOT=\"%s\"" % os.getenv("BLOSC_ROOT", install_path),
            # tbb
            "-DTBB_ROOT=\"%s\"" % os.getenv("REZ_TBB_ROOT", install_path),
            # OpenVDB needs Half type from IlmBase
            "-DILMBASE_ROOT=\"%s\"" % os.getenv("ILMBASE_ROOT", install_path),
        ]
        lib.run_cmake(source_root, install_path, extra_args=extra_args)


if __name__ == "__main__":
    build(source_path=os.environ["REZ_BUILD_SOURCE_PATH"],
          build_path=os.environ["REZ_BUILD_PATH"],
          install_path=os.environ["REZ_BUILD_INSTALL_PATH"],
          targets=sys.argv[1:])
