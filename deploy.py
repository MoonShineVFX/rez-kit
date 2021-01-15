
import os
import subprocess
from collections import OrderedDict as odict
from kitz import git, lib

from rez.config import config
from rez.utils.formatting import PackageRequest
from rez.package_repository import package_repository_manager
from rez.resolved_context import ResolvedContext
from rez.packages import (
    iter_package_families,
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


_memory = "memory@any"


def print_developer_packages(requests):
    requests = requests or []
    _before_deploy()

    names = list()
    for request in requests:
        pkg = get_latest_pkg_by_str(request, paths=[_memory])
        if pkg is None:
            print("Package not found in this repository: %s" % request)
            continue
        names.append(pkg.name)

    print("\nPackages available in this repository:")
    print("=" * 30)

    for family in iter_package_families(paths=[_memory]):
        if not requests:
            print(family.name)
        else:
            if family.name not in names:
                continue

            for package in family.iter_packages():
                print(package.qualified_name)


def deploy_packages(requests, release=False, yes=False):
    _bind("os", release)
    _bind("arch", release)
    _bind("platform", release)

    _before_deploy()

    if release:
        package_paths = config.nonlocal_packages_path + [_memory]
    else:
        package_paths = config.packages_path + [_memory]

    for request in requests:
        print("Processing deploy request: %s .." % request)
        _deploy_package(request, package_paths, release, yes)


def _before_deploy():
    _git_clone_packages()
    _developer_packages_to_memory()


def _deploy_package(request, package_paths=None, release=False, yes=False):
    implicit_pkgs = list(map(PackageRequest, config.implicit_packages))

    def in_memory(pkg):
        return pkg.parent.repository.name() == "memory"

    def dependencies_to_deploy(name):
        """"""
        is_installed = False
        to_install = odict()

        pkg_to_deploy = get_latest_pkg_by_str(name, paths=package_paths)
        if pkg_to_deploy is None:
            uri = None
            variants = []  # dev package might not exists
        else:
            name = pkg_to_deploy.qualified_name
            variants = pkg_to_deploy.iter_variants()

            if in_memory(pkg_to_deploy):
                uri = pkg_to_deploy.data.get("_uri", "??")
            else:
                uri = pkg_to_deploy.uri
                is_installed = True

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

        if not is_installed:
            to_install[name] = uri

        return to_install

    dependencies = dependencies_to_deploy(request)

    if dependencies:
        _max_name_len = len(max(dependencies.keys()))

        print("\nFollowing packages will be deployed:")
        print("-" * 70)
        for q_name, _uri in dependencies.items():
            line = " %%-%ds -> %%s" % _max_name_len
            print(line % (q_name, _uri))

        proceed = yes or lib.confirm("Do you want to continue ? [Y/n]\n")
        if not proceed:
            print("Cancelled")

        # Deploy
        for q_name, _uri in dependencies.items():
            if release:
                args = ["rez-release"]
            else:
                args = ["rez-build", "--install"]

            subprocess.check_call(args, cwd=os.path.dirname(_uri))

    else:
        print("Package %r already been installed." % request)


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
        # TODO: checkout latest
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
    # TODO: ensure vcs plugin "kit" is loaded on package release
    import sys
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument("packages", nargs="*",
                        help="Package names to deploy.")
    parser.add_argument("--release", action="store_true",
                        help="Deploy to package releasing location.")
    parser.add_argument("--yes", action="store_true",
                        help="Yes to all.")
    parser.add_argument("--list", action="store_true",
                        help="List out packages that can be deployed. If "
                        "`packages` given, versions will be listed.")

    opt = parser.parse_args()

    if opt.list:
        print_developer_packages(opt.packages)
        sys.exit(0)

    if opt.packages:
        deploy_packages(opt.packages, opt.release, opt.yes)
        print("=" * 30)
        print("SUCCESS!\n")

    else:
        print("Please name at least one package to deploy. Use --list to "
              "view available packages.")
