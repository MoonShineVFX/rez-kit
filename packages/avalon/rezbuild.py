
import os
import sys


url_prefix = "https://github.com/MoonShineVFX/avalon-core/archive"
filename = "{ver}.zip"


def build(source_path, build_path, install_path, targets=None):
    from rezutil import lib

    targets = targets or []

    if "install" in targets:
        dst = install_path + "/payload"
    else:
        dst = build_path + "/payload"

    dst = os.path.normpath(dst)

    if os.path.isdir(dst):
        lib.clean(dst)

    local_payload = os.getenv("REZ_BUILD_PKG_PAYLOAD_ROOT")
    build_version = os.environ["REZ_BUILD_PROJECT_VERSION"]
    payload_version = build_version.rsplit("-", 1)[0]

    if local_payload:
        # Source from local dev repo
        source_root = local_payload
    else:
        # Download the source
        url = "%s/%s" % (url_prefix, filename.format(ver=payload_version))
        archive = lib.download(url, filename.format(ver=payload_version))

        # Unzip the source
        source_root = lib.open_archive(archive)

    # Deploy
    # (we cannot use setup.py to install avalon, there are additional files
    # currently not being installed by it)
    lib.copy_dir(source_root, dst)

    # Additional (see getblessing/rez-avalon)
    dst_root = os.path.dirname(dst)
    for dir_name in ["apps", "bin", "python", "config", "template"]:
        dst_dir = os.path.join(dst_root, dir_name)
        lib.copy_dir(os.path.join(source_path, dir_name), dst_dir)


if __name__ == "__main__":
    build(source_path=os.environ["REZ_BUILD_SOURCE_PATH"],
          build_path=os.environ["REZ_BUILD_PATH"],
          install_path=os.environ["REZ_BUILD_INSTALL_PATH"],
          targets=sys.argv[1:])
