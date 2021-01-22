"""The Allzpark configuration file

Copy this onto your local drive and make modifications.
Anything not specified in your copy is inherited from here.

ALLZPARK_CONFIG_FILE=/path/to/allzparkconfig.py

"""

# Default filter, editable via the Preferences page
exclude_filter = "*.beta"


def profiles():
    """Return list of profiles

    This function is called asynchronously, and is suitable
    for making complex filesystem or database queries.
    Can also be a variable of type tuple or list

    """
    # collect and make in-memory profile package with eph in require
    from rez.config import config
    from rez.package_maker import PackageMaker
    from rez.packages import get_latest_package_from_string
    from rez.package_repository import package_repository_manager

    _memory = "memory@any"
    _keeper = "production-1"

    if _memory not in config.packages_path:
        config.packages_path.insert(0, _memory)

    keeper = get_latest_package_from_string(_keeper)

    _profiles = [
        "foo",
    ]

    # What about profile icon ? and other _data ?

    profile_pkgs = dict()
    for name in _profiles:
        maker = PackageMaker(name, data=keeper.data.copy())
        package = maker.get_package()
        data = package.data.copy()

        requires = data.get("requires", [])
        requires.append(".show-%s" % name)

        data["requires"] = requires
        data["version"] = "1"
        profile_pkgs[name] = {"1": data}

    memory_repo = package_repository_manager.get_repository(_memory)
    memory_repo.data = profile_pkgs

    return _profiles


def metadata_from_package(variant):
    """Return metadata relative `variant`

    Blocking call, during change of profile.

    IMPORTANT: this function must return at least the
        members part of the original function, else the program
        will not function. Very few safeguards are put in place
        in favour of performance.

    Arguments:
        variant (rez.packages_.Variant): Package from which to retrieve data

    Returns:
        dict: See function for values and types

    """

    data = getattr(variant, "_data", {})

    return dict(data, **{

        # Guaranteed keys, with default values
        "label": data.get("label", variant.name),
        "background": data.get("background"),
        "icon": data.get("icon", ""),
        "hidden": data.get("hidden", False),
    })
