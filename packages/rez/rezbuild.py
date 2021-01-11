
import os
import sys


def build(source_path, build_path, install_path, targets=None):
    import shutil

    targets = targets or []

    if "install" in targets:
        dst = install_path + "/payload"
    else:
        dst = build_path + "/payload"

    dst = os.path.normpath(dst)

    if os.path.isdir(dst):
        shutil.rmtree(dst)
    os.makedirs(dst)

    # copy source
    rez_path = os.environ["REZ_SOURCE_PATH"]
    site_path = os.path.dirname(rez_path)
    rezplugins_path = os.path.join(site_path, "rezplugins")

    shutil.copytree(rez_path, os.path.join(dst, "rez"))
    shutil.copytree(rezplugins_path, os.path.join(dst, "rezplugins"))


if __name__ == "__main__":
    build(source_path=os.environ["REZ_BUILD_SOURCE_PATH"],
          build_path=os.environ["REZ_BUILD_PATH"],
          install_path=os.environ["REZ_BUILD_INSTALL_PATH"],
          targets=sys.argv[1:])
