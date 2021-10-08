
name = "userpref"

version = "1.0-m1"

description = """Setup DCC apps user preference directory

This package will set dedicated preference directory for specific DCC
app, current supported DCC and their directory will be as follow:

* Houdini -> ${REZ_USERPREF_FIXED}/.houdiniX.Y.Z
* Maya    -> ${REZ_USERPREF_FIXED}/.maya20XY

The value of `REZ_USERPREF_FIXED` by default is user home directory,
and to define a more dedicated location, e.g. per project, the env
`REZ_USERPREF_FIXED` can be set from parent environment or via other
package.

"""
# TODO: Once rez package ecosystem is mature enough, each project/show
#   should have dedicated user dir.

build_command = False


def pre_commands():
    import os
    env = globals()["env"]
    resolve = globals()["resolve"]

    # config preference dir
    #
    pref_base = str(
            os.getenv("REZ_USERPREF_FIXED")
            or env.get("REZ_USERPREF_FIXED")
            or os.path.expanduser("~")
    )

    if "houdini" in resolve:
        # clean pref dir
        _ver = str(resolve["houdini"].version).rsplit("-")[0]
        env.HOUDINI_USER_PREF_DIR = os.path.join(
            pref_base,
            ".houdini%s" % _ver,  # may be hidden
        )

    if "maya" in resolve:
        # clean pref dir
        _ver = str(resolve["maya"].version).rsplit("-")[0]
        env.MAYA_APP_DIR = os.path.join(
            pref_base,
            ".maya%s" % _ver,  # may be hidden
        )
