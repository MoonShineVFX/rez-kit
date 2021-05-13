
import os
import sys
from rezutil import lib


url_prefix = "https://github.com/OpenImageIO/oiio/archive"
filename = "Release-1.7.14.zip"


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

    # Build
    with lib.working_dir(build_path + "/_openimageio"):
        extra_args = [
            "-DOIIO_BUILD_TOOLS=OFF",
            "-DOIIO_BUILD_TESTS=OFF",
            "-DUSE_PYTHON=OFF",
            "-DSTOP_ON_WARNING=OFF",
            # Need to specify TBB use debug or not, or release build will fail
            "-DTBB_USE_DEBUG_BUILD=%s" % ("ON" if is_debug else "OFF"),

            # OIIO's FindOpenEXR module circumvents CMake's normal library
            # search order, which causes versions of OpenEXR installed in
            # /usr/local or other hard-coded locations in the module to
            # take precedence over the version we've built, which would
            # normally be picked up when we specify CMAKE_PREFIX_PATH.
            # This may lead to undefined symbol errors at build or runtime.
            # So, we explicitly specify the OpenEXR we want to use here.
            "-DOPENEXR_HOME=\"%s\"" % os.getenv("OPENEXR_ROOT", install_path),

            "-DHDF5_ROOT=\"%s\"" % os.getenv("REZ_HDF5_ROOT", install_path),
            "-DOpenColorIO_ROOT=\"%s\"" % os.getenv("REZ_OPENCOLORIO_ROOT",
                                                    install_path),
        ]
        lib.run_cmake(source_root, install_path, extra_args=extra_args)


if __name__ == "__main__":
    build(source_path=os.environ["REZ_BUILD_SOURCE_PATH"],
          build_path=os.environ["REZ_BUILD_PATH"],
          install_path=os.environ["REZ_BUILD_INSTALL_PATH"],
          targets=sys.argv[1:])
