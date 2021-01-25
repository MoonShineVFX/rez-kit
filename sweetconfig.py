

# default suite saving root
default_root = "preset"


def suite_roots():
    """Return a dict of suite saving root path
    """
    from collections import OrderedDict as odict
    from rez.packages import get_latest_package_from_string
    from sweet import util

    _suites = "production-1"
    show_suites = get_latest_package_from_string(_suites)

    return odict([
        ("preset", util.normpath("~/rez/sweet/preset")),
        ("show", show_suites.suite_root),
    ])
