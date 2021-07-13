
name = "hou_sidefxlabs"

description = \
    """
    SideFX Labs is a completely free, open-source toolset geared towards 
    assisting Houdini users with a variety of tasks commonly used for 
    digital content creation. It is an all-inclusive toolset that spans 
    the shelf, digital assets, custom desktops and scripts and more. The 
    toolset is currently maintained by Paul Ambrosiussen and Mai Ao. It 
    also receives a lot of contributions from the always-active Houdini 
    community. The toolset originates from the GameDevelopmentToolset, 
    which got a re-launch in the Houdini 18.0 release.
    """

git_url = "https://github.com/sideeffects/SideFXLabs.git"


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
    # `SideFXLabs.json` has a field 'enable' that also checks houdini
    # version which will disable the package if not compatible.
    # So we just leave this rez requirement as minimum as what SideFXLabs
    # says.
    "houdini-18.0+",
]

private_build_requires = ["rezutil-1"]
build_command = "python {root}/rezbuild.py {install}"


def commands():
    env = globals()["env"]
    this = globals()["this"]

    payload_ver = "{}.{}.{}".format(*this.version.as_tuple()[:3])

    env.HOUDINI_PACKAGE_DIR.prepend("{root}/payload")

    env.SIDEFXLABS_ADMIN_UPDATES = "1"
    env.SIDEFXLABS_NOINSTALL_MESSAGE = (
        "SideFX Labs (%s) is provide by Rez and cannot be changed "
        "in current session." % payload_ver
    )
