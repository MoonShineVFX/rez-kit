early = globals()["early"]

name = "rez"

description = "Rez itself as package"

git_url = "https://github.com/MoonShineVFX/rez.git"


@early()
def version():
    import os

    package_ver = "m1"
    payload_ver = os.getenv("REZ_DELIVER_PKG_PAYLOAD_VER")

    if payload_ver:
        # Our fork of rez has '+' sign in version string to indicate
        # local change.
        # Which align to PEP 440 version spec but not to rez package's
        # version syntax. So we have to normalize it.
        payload_ver.replace("+", "-")

        return "%s-%s" % (
            # payload version
            payload_ver,
            # package def version
            package_ver
        )

    else:
        return "0.0.0-" + package_ver


variants = [
    ["platform-*", "arch-*", "os-*", "python-2.7"],
    ["platform-*", "arch-*", "os-*", "python-3.7"],
]

# NOTE: This build script is simply copying modules from rez source,
#       which is not robust. Better install with rez-kit deploy script.
build_command = "python {root}/rezbuild.py {install}"


def commands():
    env = globals()["env"]
    env.PYTHONPATH.append("{root}/payload")
