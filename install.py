
import os
import sys
import venv
import functools
import subprocess
from kitz import git, lib


REZ_URL = "https://github.com/MoonShineVFX/rez.git"
REZ_SRC = "build/rezsrc"

venv_pip_packages = [
    "pyside2",
    "qt.py",
    "qt5.py",
    "pymongo",
]


def install_rez(dst):
    git.clone(REZ_URL, REZ_SRC)

    rez_version = subprocess.check_output([
        sys.executable, "-c",
        "from rez.utils._version import _rez_version;print(_rez_version)"
    ], universal_newlines=True, cwd=REZ_SRC + "/src").strip()

    dst = functools.reduce(
        lambda path, f: f(path),
        [dst,
         os.path.expanduser,
         os.path.expandvars,
         os.path.normpath]
    ).format(version=rez_version)

    if os.path.isdir(dst):
        lib.clean(dst)
    os.makedirs(dst)

    subprocess.check_call([sys.executable, "install.py", "-v", dst],
                          cwd=REZ_SRC)

    install_pip_packages(dst)


def install_pip_packages(dst):
    py_executable = os.path.join(get_virtualenv_bin_dir(dst),
                                 os.path.basename(sys.executable))
    subprocess.check_call([
        py_executable, "-m", "pip", "install"] + venv_pip_packages)


def get_virtualenv_bin_dir(dest_dir):
    builder = venv.EnvBuilder()
    context = builder.ensure_directories(dest_dir)
    return context.bin_path


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument("location", nargs="?", const=True, default=None,
                        help="Rez install path if you want to install it in "
                             "custom path. If no path given, Rez will be "
                             "installed in '~/rez/core'. Directory will be "
                             "removed if exists.")
    parser.add_argument("--yes", action="store_true",
                        help="Yes to all.")

    opt = parser.parse_args()

    location = opt.location or "~/rez/core/{version}"

    print("Rez will be installed to %s" % location)
    print("Directory will be removed if exists.")
    if opt.yes or lib.confirm("Do you want to continue ? [Y/n]\n"):
        install_rez(location)
    else:
        print("Cancelled")
