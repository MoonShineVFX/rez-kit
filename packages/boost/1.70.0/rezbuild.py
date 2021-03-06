
import os
import sys
import platform
import subprocess
from rezutil import lib

PY3 = sys.version_info[0] == 3
IS_WIN = platform.system() == "Windows"
IS_LNX = platform.system() == "Linux"
IS_MAC = platform.system() == "Darwin"


url_prefix = "https://sourceforge.net/projects/boost/files/boost/1.70.0"
filename = "boost_1_70_0.tar.gz"


def with_libraries():
    return [

        "--with-atomic",
        "--with-program_options",
        "--with-regex",

        # Python
        #
        # Multiple python versions is being handled separately
        # and automatically (if any python packages installed),
        # so don't add them here.

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

    if "get-python-info" in targets:
        write_python_info()
        return

    # Download the source
    url = "%s/%s" % (url_prefix, filename)
    archive = lib.download(url, filename)

    # Unzip the source
    dont_extract = ["*/doc/*", "*/libs/*/doc/*"]
    source_root = lib.open_archive(archive,
                                   dont_extract=dont_extract)
    # Config libraries
    libraries = with_libraries()

    # Fresh user config jam
    jam_path = config_jam_path()
    if os.path.isfile(jam_path):
        os.remove(jam_path)

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
        "--user-config=%s" % jam_path,

        "install",
    ]
    set_toolset(b2_settings)

    # Look for rez python packages
    python_versions = python_config_jam()

    # Build
    with lib.working_dir(source_root):
        # specified libraries
        for variant in ["release", "debug"]:
            cmd = b2_settings + ["variant=%s" % variant]
            subprocess.check_call(cmd + libraries)

        # python
        #
        # Noted that we need to call clean build if python 2 and 3 both
        # being presented.
        # https://stackoverflow.com/a/28893295/4145300
        #
        previous_major = None
        for py_ver in python_versions:
            major = py_ver.split(".")[0]
            need_clean = previous_major and previous_major != major
            previous_major = major

            py_libs = ["--with-python", "python=%s" % py_ver]
            # if major == "3":
            #     py_libs.append("--buildid=3")

            if need_clean:
                subprocess.check_call(cmd + py_libs + ["--clean"])

            for variant in ["release", "debug"]:
                cmd = b2_settings + ["variant=%s" % variant]
                subprocess.check_call(cmd + py_libs)


def config_jam_path():
    file_name = "user-config.jam"
    return os.path.join(os.environ["REZ_BUILD_PATH"], file_name)


def append_config_jam(line):
    with open(config_jam_path(), "a") as jam:
        jam.write(line)


def set_toolset(settings):
    if IS_MAC:
        settings.append("toolset=clang")


def python_config_jam():
    # Lookup all installed python packages
    from rez import packages, resolved_context

    versions = list()

    info_cmd = ("python %s get-python-info" % sys.argv[0])

    for python_pkg in packages.iter_packages("python"):
        full_ver = str(python_pkg.version)
        python_ver = ".".join(full_ver.split(".")[:2])  # exclude patch ver
        versions.append(python_ver)

    versions.sort()
    # Only use python-27 for now (for USD)
    #   because cmake files only link to the version which built latest.
    versions = ["2.7"]

    for python_ver in versions:
        python_name = "python-%s" % python_ver
        rc = resolved_context.ResolvedContext([python_name], caching=False)
        popen = rc.execute_shell(command=info_cmd)
        popen.wait()

    return versions


def write_python_info():
    info = lib.python_info()

    if IS_WIN:
        # Unfortunately Boost build scripts require the Python folder
        # that contains the executable on Windows
        python_path = os.path.dirname(info[0])
    else:
        # While other platforms want the complete executable path
        python_path = info[0]

    # This is the only platform-independent way to configure these
    # settings correctly and robustly for the Boost jam build system.
    # There are Python config arguments that can be passed to bootstrap
    # but those are not available in boostrap.bat (Windows) so we must
    # take the following approach:
    line = 'using python : %s : "%s" : "%s" ;\n' % (
        # Note that we must escape any special characters, like
        # backslashes for jam, hence the mods below for the path
        # arguments. Also, if the path contains spaces jam will not
        # handle them well. Surround the path parameters in quotes.
        info[3],
        python_path.replace('\\', '\\\\'),
        info[2].replace('\\', '\\\\')
    )
    append_config_jam(line)


if __name__ == "__main__":
    build(source_path=os.environ["REZ_BUILD_SOURCE_PATH"],
          build_path=os.environ["REZ_BUILD_PATH"],
          install_path=os.environ["REZ_BUILD_INSTALL_PATH"],
          targets=sys.argv[1:])
