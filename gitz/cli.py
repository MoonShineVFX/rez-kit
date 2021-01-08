
import os
import sys
import time
import shutil
import logging
import tempfile
import argparse

from . import git

log = logging.getLogger("gitz")
log.setLevel(logging.INFO)


def tell(msg, newlines=1):
    if log.level == logging.CRITICAL:
        return

    import sys
    sys.stdout.write("%s%s" % (msg, "\n" * newlines))


def main(argv=None):
    argv = argv or sys.argv

    # Mute unnecessary messages
    logging.basicConfig(format="%(levelname)-8s %(message)s")
    logging.getLogger("rez.vendor.distlib").setLevel(logging.CRITICAL)

    parser = argparse.ArgumentParser(description="git for Rez")
    parser.add_argument(
        "url",
        help="Git repository URL")
    parser.add_argument(
        "--branch",
        help="Clone on specific branch")
    parser.add_argument(
        "--install", action="store_true",
        help="Install the package")
    parser.add_argument(
        "--release", action="store_true",
        help="Install as released package; if not set, package is installed "
        "locally only")
    parser.add_argument(
        "--build-options", nargs="+",
        help="Rez package build options")
    parser.add_argument(
        "-q", "--quiet", action="store_true",
        help="Do not output anything to stdout")
    parser.add_argument(
        "-v", "--verbose", action="store_true",
        help="Print more information to the screen")
    parser.add_argument(
        "--debug", action="store_true",
        help="Do not clean up temporary files")

    opts = parser.parse_args(argv[1:])

    if opts.verbose:
        log.setLevel(logging.DEBUG)

    if opts.quiet:
        log.setLevel(logging.CRITICAL)

    t0 = time.time()
    tmpdir = tempfile.mkdtemp()
    tempdir = os.path.join(tmpdir, "git")

    try:
        git.build(opts.url, tempdir, opts.branch,
                  opts.install, opts.release, opts.build_options)
    except Exception:
        success = False
    else:
        success = True
    finally:
        if opts.debug:
            tell("Temporary files @ %s" % tmpdir)
        else:
            shutil.rmtree(tmpdir)

    tell(
        ("Completed in %.2fs" % (time.time() - t0))
        if success else "Failed"
    )

    return success
