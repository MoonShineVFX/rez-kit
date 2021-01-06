
import os
import sys
import stat
import shutil
import platform


bash = """
#!/usr/bin/env bash
python -u -m mockapp {tool}
"""

cmd = """
@echo off
call python -u -m mockapp {tool}
"""


def build(source_path, build_path, install_path, targets=None):
    import identicon

    targets = targets or []

    if "install" in targets:
        targets.remove("install")
        dst = install_path
    else:
        dst = build_path

    dst = os.path.normpath(dst)

    if os.path.isdir(dst):
        shutil.rmtree(dst)
    os.makedirs(dst)

    dir_src = os.path.join(source_path, "python")
    dir_dst = os.path.join(dst, "python")
    shutil.copytree(dir_src, dir_dst)

    tools = targets

    if platform.system() == "Windows":
        script = cmd
        ext = ".bat"
    else:
        script = bash
        ext = ""

    bin_dir = os.path.join(dst, "bin")
    os.makedirs(bin_dir)
    for tool in tools:
        bin_path = os.path.join(bin_dir, tool) + ext
        with open(bin_path, "w") as bin_:
            bin_.write(script.format(tool=tool))

        # chmod +x
        st = os.stat(bin_path)
        os.chmod(bin_path, st.st_mode | stat.S_IEXEC)

    res_dir = os.path.join(dst, "resources")
    os.makedirs(res_dir)

    # generate identicon from app name-version
    ident = "%s-%s" % (os.environ["REZ_BUILD_PROJECT_NAME"],
                       os.environ["REZ_BUILD_PROJECT_VERSION"])
    icon_path = identicon.generate(ident)
    shutil.move(icon_path, os.path.join(res_dir, "icon.png"))


if __name__ == "__main__":
    build(source_path=os.environ["REZ_BUILD_SOURCE_PATH"],
          build_path=os.environ["REZ_BUILD_PATH"],
          install_path=os.environ["REZ_BUILD_INSTALL_PATH"],
          targets=sys.argv[1:])
