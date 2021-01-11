
import os
import subprocess
from collections import OrderedDict as odict
from gitz import git

from rez.config import config
from rez.utils.formatting import PackageRequest
from rez.package_repository import package_repository_manager
from rez.resolved_context import ResolvedContext
from rez.packages import (
    iter_package_families,
    get_developer_package,
    get_latest_package_from_string as get_latest_pkg_by_str,
)


_root = os.path.dirname(os.path.abspath(__file__))
_dev_dirs = [
    # dir name must be valid Rez package name
    os.path.join(_root, "packages"),
    os.path.join(_root, "downloads"),
]

_pkg_repos = [
    {
        "name": "pipz",
        "url": "https://github.com/davidlatwe/rez-pipz.git",
        "branch": "dev",
    },
]


def list_developer_packages():
    packages = list()

    for family in iter_package_families(paths=_dev_dirs):
        for package in family.iter_packages():
            pkg_dir = os.path.dirname(package.uri)
            package = get_developer_package(pkg_dir)

            packages.append(package)

    return packages


_memory = "memory@any"


def deploy_package(request, release=False):
    _bind("os", release)
    _bind("arch", release)
    _bind("platform", release)

    _git_clone_packages()
    _developer_packages_to_memory()

    implicit_pkgs = [PackageRequest(x) for x in config.implicit_packages]
    implicit_pkgs = list(map(PackageRequest, config.implicit_packages))

    if release:
        package_paths = config.nonlocal_packages_path + [_memory]
    else:
        package_paths = config.packages_path + [_memory]

    def in_memory(pkg):
        return pkg.parent.repository.name() == "memory"

    def dependencies_to_deploy(name):
        """"""
        to_install = odict()

        pkg_to_deploy = get_latest_pkg_by_str(name, paths=package_paths)
        if pkg_to_deploy is None:
            uri = None
            variants = []  # dev package might not exists
        else:
            name = pkg_to_deploy.qualified_name

            if in_memory(pkg_to_deploy):
                uri = pkg_to_deploy.data.get("_uri", "??")
                variants = pkg_to_deploy.iter_variants()
            else:
                uri = pkg_to_deploy.uri
                variants = []  # already installed, escape early

        for variant in variants:
            pkg_requests = variant.get_requires(build_requires=True,
                                                private_build_requires=True)

            context = ResolvedContext(pkg_requests + implicit_pkgs,
                                      building=True,
                                      package_paths=package_paths)

            for package in context.resolved_packages:
                dep_name = package.qualified_package_name

                if in_memory(package):
                    # need install
                    to_install.update(dependencies_to_deploy(dep_name))

                else:
                    # already installed
                    pass

        to_install[name] = uri
        return to_install

    dependencies = dependencies_to_deploy(request)
    _max_name_len = len(max(dependencies.keys()))

    print("\nFollowing packages will be deployed:")
    print("-" * 70)
    for q_name, _uri in dependencies.items():
        line = " %%-%ds -> %%s" % _max_name_len
        print(line % (q_name, _uri))

    # Deploy
    for q_name, _uri in dependencies.items():
        if release:
            args = ["rez-release"]
        else:
            args = ["rez-build", "--install"]

        subprocess.check_call(args, cwd=os.path.dirname(_uri))


def _memory_repository(packages):
    repository = package_repository_manager.get_repository(_memory)
    repository.data = packages


def _developer_packages_to_memory():
    packages = dict()

    for family in iter_package_families(paths=_dev_dirs):
        name = family.name  # package dir name
        versions = dict()

        for package in family.iter_packages():
            data = package.data.copy()
            name = data["name"]  # real name in package.py

            version = data.get("version", "")
            data["_uri"] = package.uri
            versions[version] = data

        packages[name] = versions

    _memory_repository(packages)


def _git_clone_packages():
    for repo in _pkg_repos:
        git.clone(
            url=repo["url"],
            dst=os.path.join(_root, "downloads", repo["name"]),
            branch=repo["branch"],
        )


def _bind(name, release=False):
    if release:
        paths = config.nonlocal_packages_path
        pkg = get_latest_pkg_by_str(name, paths=paths)
        if pkg is None:
            subprocess.check_call(["rez-bind", "--release", name])
    else:
        paths = config.packages_path
        pkg = get_latest_pkg_by_str(name, paths=paths)
        if pkg is None:
            subprocess.check_call(["rez-bind", name])


if __name__ == "__main__":
    # deploy_package("usd-20.08", release=True)
    # deploy_package("maya-2020")
    deploy_package("Qt.py")
    # deploy_package("rez")
