"""The Allzpark configuration file

Copy this onto your local drive and make modifications.
Anything not specified in your copy is inherited from here.

ALLZPARK_CONFIG_FILE=/path/to/allzparkconfig.py

"""


def profiles():
    # collect and make in-memory profile package with eph in require
    import os
    from rez.config import config
    from rez.package_maker import PackageMaker
    from rez.packages import get_latest_package_from_string
    from rez.package_repository import package_repository_manager

    _memory = "memory@any"
    _suites = "production-1"
    _profiles = []

    if _memory not in config.packages_path:
        config.packages_path.insert(0, _memory)

    suites = get_latest_package_from_string(_suites)

    profile_pkgs = dict()
    for name in os.listdir(suites.suite_root):
        maker = PackageMaker(name, data=suites.data.copy())
        package = maker.get_package()
        data = package.data.copy()

        requires = data.get("requires", [])
        requires.append(".show-%s" % name)

        data["requires"] = requires
        data["version"] = "1"
        profile_pkgs[name] = {"1": data}

        _profiles.append(name)

    memory_repo = package_repository_manager.get_repository(_memory)
    memory_repo.data = profile_pkgs

    return _profiles
