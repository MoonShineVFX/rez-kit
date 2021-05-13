
import os
import sys
import platform
import subprocess
from rezutil import lib

PY3 = sys.version_info[0] == 3
IS_WIN = platform.system() == "Windows"
IS_LNX = platform.system() == "Linux"
IS_MAC = platform.system() == "Darwin"


url_prefix = "https://sourceforge.net/projects/boost/files/boost/1.65.1"
filename = "boost_1_65_1.tar.gz"


def with_libraries():
    return [

        "--with-atomic",
        "--with-program_options",
        "--with-regex",

        # Python
        "--with-python",

        # OIIO
        "--with-date_time",
        "--with-filesystem",

        # OpenVDB
        #
        # b2 with -sNO_COMPRESSION=1 fails with the following error message:
        #     error: at [...]/boost_1_61_0/tools/build/src/kernel/modules.jam:107
        #     error: Unable to find file or target named
        #     error:     '/zlib//zlib'
        #     error: referred to from project at
        #     error:     'libs/iostreams/build'
        #     error: could not resolve project reference '/zlib'
        #
        # But to avoid an extra library dependency, we can still explicitly
        # exclude the bzip2 compression from boost_iostreams
        # (note that OpenVDB uses blosc compression).
        "-sNO_BZIP2=1",
        "--with-iostreams",

        # OIIO or OpenVDB
        "--with-system",
        "--with-thread",

    ]


def build(source_path, build_path, install_path, targets):
    targets = targets or []
    if "install" not in targets:
        install_path = build_path + "/install"

    is_debug = lib.is_debug_build()

    # Download the source
    url = "%s/%s" % (url_prefix, filename)
    archive = lib.download(url, filename)

    # Unzip the source
    dont_extract = ["*/doc/*", "*/libs/*/doc/*"]
    source_root = lib.open_archive(archive, cleanup=True,
                                   dont_extract=dont_extract)
    # Config libraries
    libraries = with_libraries()

    # Bootstrap
    with lib.working_dir(source_root):
        bootstrap = "bootstrap.bat" if IS_WIN else "./bootstrap.sh"
        subprocess.check_call([bootstrap, "--prefix=%s" % install_path])

    # Run B2
    b2_exec = "b2" if IS_WIN else "./b2"
    b2_settings = [
        b2_exec,
        "--prefix=%s" % install_path,
        "--build-dir=%s" % build_path + "/build",
        # avoid 'path too long' fail on Windows
        "--hash",
        "-j%s" % os.environ["REZ_BUILD_THREAD_COUNT"],

        "address-model=64",
        "link=shared",
        "runtime-link=shared",
        "threading=multi",

        "install",
        "variant=%s" % ("debug" if is_debug else "release"),
    ]
    set_toolset(b2_settings)

    # Build
    with lib.working_dir(source_root):
        subprocess.check_call(b2_settings + libraries)


def set_toolset(settings):
    if IS_MAC:
        settings.append("toolset=clang")


if __name__ == "__main__":
    build(source_path=os.environ["REZ_BUILD_SOURCE_PATH"],
          build_path=os.environ["REZ_BUILD_PATH"],
          install_path=os.environ["REZ_BUILD_INSTALL_PATH"],
          targets=sys.argv[1:])
