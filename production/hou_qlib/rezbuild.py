
import os
import sys
import shutil


url_prefix = "https://github.com/qLab/qLib/archive"
payload = "{ver}.zip"


def build(source_path, build_path, install_path, targets=None):
    import ast
    import json
    import platform
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

    # Correcting package path
    settings_file_win = os.path.join(source_root, "qLib_package_windows.json")
    settings_file_lnx = os.path.join(source_root, "qLib_package_linux.json")
    settings_file = settings_file_win \
        if platform.system() == "Windows" else settings_file_lnx

    if not os.path.isfile(settings_file):
        raise Exception("qLib package file not exists: %s"
                        % settings_file)

    with open(settings_file, "r") as f:
        # qLib's package file contains JSON invalid trailing comma, and that
        # makes it cannot be loaded via `json.load`. So as a workaround we
        # use `ast.literal_eval` instead, since that package file doesn't
        # has values like None, True or False which cannot be parsed with
        # `ast` module.
        settings = ast.literal_eval(f.read())

    settings["version"] = payload_version
    for env in settings["env"]:
        if "QLIB" in env:
            # NOTE:
            #   $HOUDINI_PACKAGE_PATH variable is generated by Houdini and
            #   the value is the location of current package file.
            env["QLIB"] = "$HOUDINI_PACKAGE_PATH"
            break

    with open(os.path.join(source_root, "qLib.json"), "w") as f:
        json.dump(settings, f, indent=4)
    os.remove(settings_file_win)
    os.remove(settings_file_lnx)

    # Remove updater
    #   qLib doesn't have a switch like SideFXLabs has that could turn off
    #   the update button for site-wide management. So we just remove that
    #   shelf script.
    updater_shelf = os.path.join(source_root, "toolbar", "qLib-update.shelf")
    os.remove(updater_shelf)

    # Deploy
    shutil.copytree(source_root, dst)


if __name__ == "__main__":
    build(source_path=os.environ["REZ_BUILD_SOURCE_PATH"],
          build_path=os.environ["REZ_BUILD_PATH"],
          install_path=os.environ["REZ_BUILD_INSTALL_PATH"],
          targets=sys.argv[1:])
