
import os
import sys
import shutil


url_prefix = "https://github.com/sideeffects/SideFXLabs/archive"
payload = "{ver}.zip"


def build(source_path, build_path, install_path, targets=None):
    from rezutil import lib

    targets = targets or []

    if "install" in targets:
        dst = install_path + "/payload"
    else:
        dst = build_path + "/payload"

    dst = os.path.normpath(dst)

    if os.path.isdir(dst):
        shutil.rmtree(dst)

    build_version = os.environ["REZ_BUILD_PROJECT_VERSION"]
    payload_version = build_version.rsplit("-", 1)[0]

    # Download the source
    url = "%s/%s" % (url_prefix, payload.format(ver=payload_version))
    archive = lib.download(url, os.path.basename(url))

    # Unzip the source
    source_root = lib.open_archive(archive)

    # Deploy
    shutil.copytree(source_root, dst)


if __name__ == "__main__":
    build(source_path=os.environ["REZ_BUILD_SOURCE_PATH"],
          build_path=os.environ["REZ_BUILD_PATH"],
          install_path=os.environ["REZ_BUILD_INSTALL_PATH"],
          targets=sys.argv[1:])
