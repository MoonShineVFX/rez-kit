
import os
import sys
import logging
import subprocess


PY3 = sys.version_info[0] == 3
log = logging.getLogger("gitz")


def clone(url, dst, branch=None, single_branch=True):
    # https://stackoverflow.com/a/4568323/14054728

    if os.path.isdir(dst + "/.git"):
        print("git dir exists, skip clone.")
        return

    args = ["git", "clone"]

    if branch:
        args.extend(["-b", branch])

    if single_branch:
        args.append("--single-branch")

    args.extend([url, dst])

    subprocess.check_output(args)


def get_branch(repository):
    branch = subprocess.check_output(["git", "branch"], cwd=repository)
    if PY3:
        branch = branch.decode()

    return branch[len("* "):].strip()


def build(url, clone_dst, branch=None,
          install=False, release=False, build_options=None):

    clone(url, dst=clone_dst, branch=branch)

    branch = get_branch(clone_dst)
    log.info("Cloned branch: [%s]" % branch)

    package_py = os.path.join(clone_dst, "package.py")
    if not os.path.isfile(package_py):
        raise Exception("Rez package.py not found")

    # build

    if release:
        args = ["rez-release"]
    else:
        args = ["rez-build"]
        if install:
            args.append("--install")

    args.extend(build_options or [])

    subprocess.check_call(args, cwd=clone_dst)
