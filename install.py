
import os
import sys
import functools
import subprocess
from gitz import git, lib


REZ_URL = "https://github.com/nerdvegas/rez.git"


def install_rez(dst):
    rezsrc = "build/rezsrc"
    git.clone(REZ_URL, rezsrc)

    if os.path.isdir(dst):
        lib.clean(dst)
    os.makedirs(dst)

    subprocess.check_call([sys.executable, "install.py", "-v", dst],
                          cwd=rezsrc)


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

    location = functools.reduce(lambda path, f: f(path),
                                [opt.location or "~/rez/core",
                                 os.path.expanduser,
                                 os.path.expandvars,
                                 os.path.normpath])

    print("Rez will be installed to %s" % location)
    print("Directory will be removed if exists.")
    if opt.yes or lib.confirm("Do you want to continue ? [Y/n]\n"):
        install_rez(location)
    else:
        print("Cancelled")
