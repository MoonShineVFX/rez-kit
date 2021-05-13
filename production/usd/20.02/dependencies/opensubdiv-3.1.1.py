
import os
import sys
from rezutil import lib


url_prefix = "https://github.com/PixarAnimationStudios/OpenSubdiv/archive"
filename = "v3_1_1.zip"


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
    with lib.working_dir(build_path + "/_opensubdiv"):
        extra_args = [
            "-DNO_EXAMPLES=ON",
            "-DNO_TUTORIALS=ON",
            "-DNO_REGRESSION=ON",
            "-DNO_DOC=ON",
            "-DNO_OMP=ON",
            "-DNO_CUDA=ON",
            "-DNO_OPENCL=ON",
            "-DNO_DX=ON",
            "-DNO_TESTS=ON",
            "-DNO_GLEW=ON",
            "-DNO_GLFW=ON",
        ]
        lib.run_cmake(source_root, install_path, extra_args=extra_args)


if __name__ == "__main__":
    build(source_path=os.environ["REZ_BUILD_SOURCE_PATH"],
          build_path=os.environ["REZ_BUILD_PATH"],
          install_path=os.environ["REZ_BUILD_INSTALL_PATH"],
          targets=sys.argv[1:])
