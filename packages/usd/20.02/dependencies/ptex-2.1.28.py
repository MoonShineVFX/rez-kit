
import os
import sys
import platform
from rezutil import lib

IS_WIN = platform.system() == "Windows"


url_prefix = "https://github.com/wdas/ptex/archive"
filename = "v2.1.28.zip"


def build(source_path, build_path, install_path, targets):
    targets = targets or []
    if "install" not in targets:
        install_path = build_path + "/install"

    # Download the source
    url = "%s/%s" % (url_prefix, filename)
    archive = lib.download(url, filename)

    # Unzip the source
    source_root = lib.open_archive(archive)

    if IS_WIN:
        win_patch(source_root)

    # Build
    with lib.working_dir(build_path + "/_ptex"):
        lib.run_cmake(source_root, install_path)


def win_patch(source):
    # Ptex has a bug where the import library for the dynamic library and
    # the static library both get the same name, Ptex.lib, and as a
    # result one clobbers the other. We hack the appropriate CMake
    # file to prevent that. Since we don't need the static library we'll
    # rename that.
    #
    # In addition src\tests\CMakeLists.txt adds -DPTEX_STATIC to the
    # compiler but links tests against the dynamic library, causing the
    # links to fail. We patch the file to not add the -DPTEX_STATIC
    lib.patch_file(
        source + "/src/ptex/CMakeLists.txt",
        [("set_target_properties(Ptex_static PROPERTIES OUTPUT_NAME Ptex)",
         "set_target_properties(Ptex_static PROPERTIES OUTPUT_NAME Ptexs)")]
    )
    lib.patch_file(
        source + "/src/tests/CMakeLists.txt",
        [("add_definitions(-DPTEX_STATIC)",
          "# add_definitions(-DPTEX_STATIC)")]
    )

    # Patch Ptex::String to export symbol for operator<<
    # This is required for newer versions of OIIO, which make use of the
    # this operator on Windows platform specifically.
    lib.patch_file(
        source + "/src/ptex/Ptexture.h",
        [("std::ostream& operator << (std::ostream& stream, const Ptex::String& str);",
          "PTEXAPI std::ostream& operator << (std::ostream& stream, const Ptex::String& str);")]
    )


if __name__ == "__main__":
    build(source_path=os.environ["REZ_BUILD_SOURCE_PATH"],
          build_path=os.environ["REZ_BUILD_PATH"],
          install_path=os.environ["REZ_BUILD_INSTALL_PATH"],
          targets=sys.argv[1:])
