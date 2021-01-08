
import os
import subprocess
from gitz import git

from rez.config import config
from rez.utils.formatting import PackageRequest
from rez.package_repository import package_repository_manager
from rez.resolved_context import ResolvedContext
from rez.packages import (
    iter_package_families,
    get_developer_package,
    get_latest_package_from_string,
)


_root = os.path.dirname(os.path.abspath(__file__))
_dev_dirs = [
    os.path.join(_root, "packages"),
]


def deploy_pipz(release=False):
    git.build(
        "https://github.com/davidlatwe/rez-pipz.git",
        branch="dev",
        clone_dst="build/pipz",
        install=True,
        release=release,
    )


def list_developer_packages():
    packages = list()

    for family in iter_package_families(paths=_dev_dirs):
        for package in family.iter_packages():
            pkg_dir = os.path.dirname(package.uri)
            package = get_developer_package(pkg_dir)

            packages.append(package)

    return packages


def find_developer_package(request_txt):
    return get_latest_package_from_string(request_txt, paths=_dev_dirs)


_memory = "memory@any"


def deploy_package(request, release=False):
    _bind("os", release)
    _bind("arch", release)
    _bind("platform", release)
    _developer_packages_to_memory()

    requested_package = find_developer_package(request)

    implicit_packages = [
        PackageRequest(x) for x in config.implicit_packages
    ]
    if release:
        package_paths = config.nonlocal_packages_path + [_memory]
    else:
        package_paths = config.packages_path + [_memory]

    for variant in requested_package.iter_variants():
        package_requests = variant.get_requires(build_requires=True,
                                                private_build_requires=True)

        context = ResolvedContext(package_requests + implicit_packages,
                                  building=True,
                                  package_paths=package_paths)

        for package in context.resolved_packages:
            print(package.qualified_package_name)


def _memory_repository(packages):
    repository = package_repository_manager.get_repository(_memory)
    repository.data = packages


def _developer_packages_to_memory():
    packages = dict()

    for family in iter_package_families(paths=_dev_dirs):
        versions = dict()

        for package in family.iter_packages():
            version = package.data.get("version", "")
            versions[version] = package.data

        packages[family.name] = versions

    _memory_repository(packages)


def _bind(name, release=False):
    if release:
        paths = config.nonlocal_packages_path
        pkg = get_latest_package_from_string(name, paths=paths)
        if pkg is None:
            subprocess.check_call(["rez-bind", "--release", name])
    else:
        paths = config.packages_path
        pkg = get_latest_package_from_string(name, paths=paths)
        if pkg is None:
            subprocess.check_call(["rez-bind", name])


if __name__ == "__main__":
    deploy_package("usd-20.08", release=True)
    # deploy_package("maya-2020")
