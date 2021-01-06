
import os
import sys
from rezutil import lib


url_prefix = "https://github.com/AcademySoftwareFoundation/openexr/archive"
filename = "v2.2.0.zip"


def build(source_path, build_path, install_path, targets):
    targets = targets or []
    if "install" not in targets:
        install_path = build_path + "/install"

    # Download the source
    url = "%s/%s" % (url_prefix, filename)
    archive = lib.download(url, filename)

    # Unzip the source
    source_root = lib.open_archive(archive)

    ilm_source_root = os.path.join(source_root, "IlmBase")
    exr_source_root = os.path.join(source_root, "OpenEXR")

    # Build ilmbase
    with lib.working_dir(build_path + "/_ilmbase"):
        lib.run_cmake(ilm_source_root, install_path)

    # Build openexr
    with lib.working_dir(build_path + "/_openexr"):
        os.environ["PATH"] += ";" + install_path + "/lib"  # find ilmbase
        extra_args = [
            "-DILMBASE_PACKAGE_PREFIX=\"%s\"" % install_path
        ]
        lib.run_cmake(exr_source_root, install_path, extra_args=extra_args)


if __name__ == "__main__":
    build(source_path=os.environ["REZ_BUILD_SOURCE_PATH"],
          build_path=os.environ["REZ_BUILD_PATH"],
          install_path=os.environ["REZ_BUILD_INSTALL_PATH"],
          targets=sys.argv[1:])
