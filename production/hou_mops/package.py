
name = "hou_mops"

description = "Motion OPerators for Houdini, a motion graphics toolkit. "\
              "See https://github.com/toadstorm/MOPS"

git_url = "https://github.com/toadstorm/MOPS.git"


@early()
def version():
    import os

    package_ver = "m2"
    payload_ver = os.getenv("REZ_DELIVER_PKG_PAYLOAD_VER")

    if payload_ver:
        return "%s-%s" % (
            # payload version
            payload_ver,
            # package def version
            package_ver
        )

    else:
        return "0.0.0-" + package_ver


requires = [
    # From MOPs README:
    #   Houdini 18.5 builds after 18.5.351 have an error that prevents
    #   packages from loading properly. If you are using Houdini 18.5,
    #   you must either download build 18.5.415 or later, or use the
    #   Houdini.env installation method.
    "houdini-17.5+<18.5.351|18.5.415+",
]

private_build_requires = ["rezutil-1"]
build_command = "python {root}/rezbuild.py {install}"


def commands():
    env = globals()["env"]
    env.HOUDINI_PACKAGE_DIR.prepend("{root}/payload")
