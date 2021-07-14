
name = "hou_qlib"

description = \
    """
    qLib is a digital asset library for SideFX's Houdini. It is a collection 
    of tools designed to work flawlessly with each other and Houdini's native 
    toolset. It is driven by (and used in) real production environments, but 
    at the same time it fully respects and conforms to all the important 
    Houdini concepts.

    Strong emphasis on the following things:

    * Backwards-compatibility: old scenes will not break over time
    * Performance: we press for VEX/multithreading as much as possible
    * Usability: our tools try to avoid the "in-house" look-and-feel
    
    qLib is open source software licensed under the New BSD license. It's 
    developed by VFX professionals from several studios working on feature 
    films, game cinematics and commercials.
    """

git_url = "https://github.com/qLab/qLib.git"


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
    # qLab says qLib is always backward compatible, as long as Houdini meets
    # the minimum requirement (higher than or equal to 17.5.321)
    "houdini-17.5.321+",
]

variants = [
    ["platform-*"],
]

private_build_requires = ["rezutil-1"]
build_command = "python {root}/rezbuild.py {install}"


def commands():
    env = globals()["env"]

    env.QLIB = "{root}/payload"
    env.QOTL = "{root}/payload/otls"
    env.HOUDINI_OTLSCAN_PATH.prepend("{root}/payload/otls/experimental")
    env.HOUDINI_OTLSCAN_PATH.prepend("{root}/payload/otls/future")
    env.HOUDINI_OTLSCAN_PATH.prepend("{root}/payload/otls/base")
    env.HOUDINI_PATH.prepend("{root}/payload")
