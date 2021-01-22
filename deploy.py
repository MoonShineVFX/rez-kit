
import os
import logging
import subprocess
from collections import OrderedDict as odict
from kitz import git, lib
from install import REZ_SRC


_state = dict()
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
    {
        "name": "house",
        "url": "https://github.com/MoonShineVFX/rez-house.git",
        # This is private repo
    },
    {
        "name": "production",
        "url": "https://github.com/MoonShineVFX/rez-production.git",
    },
]


_memory = "memory@any"


def set_release(value):
    from rez.config import config

    if value:
        _state.update({
            "release": True,
            "bind_cmd": ["rez-bind", "--release"],
            "install_cmd": ["rez-release"],
            "packages_path": config.nonlocal_packages_path[:],
            "install_path": config.release_packages_path,
        })
    else:
        _state.update({
            "release": False,
            "bind_cmd": ["rez-bind"],
            "install_cmd": ["rez-build", "--install"],
            "packages_path": config.packages_path[:],
            "install_path": config.local_packages_path,
        })


def print_developer_packages(requests):
    from rez.utils.logging_ import logger
    from rez.packages import (
        iter_package_families,
        get_latest_package_from_string,
    )

    logger.setLevel(logging.WARNING)

    requests = requests or []
    _before_deploy()

    names = list()
    for request in requests:
        pkg = get_latest_package_from_string(request, paths=[_memory])
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


def deploy_packages(requests, yes=False):
    from rez.utils.logging_ import logger

    logger.setLevel(logging.WARNING)

    _bind("os")
    _bind("arch")
    _bind("platform")

    _before_deploy()

    package_paths = _state["packages_path"] + [_memory]

    for request in requests:
        print("Processing deploy request: %s .." % request)
        deployed = _deploy_package(request, package_paths, yes)
        if not deployed:
            break
    else:
        return True


def _before_deploy():
    _git_clone_packages()
    _developer_packages_to_memory()


def _clear_repo_cache(path=None):
    """Clear filesystem repo family cache after pkg bind/install

    Current use case: Clear cache after rez-bind and before iter dev
    packages into memory. Without this, variants like os-* may not be
    expanded due to filesystem repo doesn't know 'os' has been bind since
    the family list is cached in this session.

    """
    from rez.package_repository import package_repository_manager

    path = path or _state["install_path"]
    fs_repo = package_repository_manager.get_repository(path)
    fs_repo.get_family.cache_clear()


def _deploy_package(request, package_paths=None, yes=False):
    from rez.packages import get_latest_package_from_string

    def in_memory(pkg):
        return pkg.parent.repository.name() == "memory"

    def dependencies_to_deploy(name):
        """"""
        is_installed = False
        to_install = odict()

        pkg_to_deploy = get_latest_package_from_string(name,
                                                       paths=package_paths)
        if pkg_to_deploy is None:
            uri = None
            variants = []  # dev package might not exists
        else:
            name = pkg_to_deploy.qualified_name
            variants = pkg_to_deploy.iter_variants()
            # TODO: check all variants are installed

            if in_memory(pkg_to_deploy):
                uri = pkg_to_deploy.data.get("_uri", "??")
            else:
                uri = pkg_to_deploy.uri
                is_installed = True

        for variant in variants:
            context = _get_build_context(variant, package_paths)
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
            return

        # Deploy
        for q_name, _uri in dependencies.items():
            if q_name.startswith("rez-"):
                _clear_repo_cache()
                _install_rez_as_package(package_paths)
                continue

            args = _state["install_cmd"]
            subprocess.check_call(args, cwd=os.path.dirname(_uri))

    else:
        print("Package %r already been installed." % request)

    return True


def _get_build_context(variant, package_paths=None):
    from rez.config import config
    from rez.utils.formatting import PackageRequest
    from rez.resolved_context import ResolvedContext

    implicit_pkgs = list(map(PackageRequest, config.implicit_packages))
    pkg_requests = variant.get_requires(build_requires=True,
                                        private_build_requires=True)
    return ResolvedContext(pkg_requests + implicit_pkgs,
                           building=True,
                           package_paths=package_paths)


def _install_rez_as_package(package_paths):
    """Use Rez's install script to deploy rez as package
    """
    from rez.packages import get_latest_package_from_string

    rez_install = os.path.join(os.path.abspath(REZ_SRC), "install.py")
    dev_pkg = get_latest_package_from_string("rez", paths=[_memory])
    dst = _state["install_path"]

    print("Installing Rez as package..")

    for variant in dev_pkg.iter_variants():
        print("Variant: ", variant)

        context = _get_build_context(variant, package_paths)
        context.execute_shell(
            command=["python", rez_install, "-v", "-p", dst],
            block=True,
            cwd=REZ_SRC,
        )


def _developer_packages_to_memory():
    """Collect and save developer packages into memory repository

    By making packages from developer packages, and saving them into Rez's
    memory repository, we can then resolve requests to see if any package
    is resolved from memory, and deployed it.

    """
    from rez.config import config
    from rez.package_maker import PackageMaker
    from rez.packages import iter_package_families
    from rez.developer_package import DeveloperPackage
    from rez.package_repository import package_repository_manager

    packages = dict()

    # Append _dev_dirs into packages_path so the requires can be expanded.
    # If we don't do this, requirements like "os-*" or "python-2.*" may fail
    # the schema validation due to the required package is not yet installed.
    config.override("packages_path", config.packages_path[:] + _dev_dirs)
    # Ensure unversioned package is allowed, so we can iter dev packages.
    config.override("allow_unversioned_packages", True)

    for family in iter_package_families(paths=_dev_dirs):
        name = family.name  # package dir name
        versions = dict()

        for _pkg in family.iter_packages():
            data = _pkg.data.copy()
            name = data["name"]  # real name in package.py

            maker = PackageMaker(name,
                                 data=data,
                                 package_cls=DeveloperPackage)
            package = maker.get_package()
            data = package.data.copy()

            # preprocessing
            result = package._get_preprocessed(data)
            if result:
                package, data = result

            data["_uri"] = _pkg.uri
            version = data.get("version", "unversioned")
            versions[version] = data

        packages[name] = versions

    # save collected dev packages in memory repository
    memory_repo = package_repository_manager.get_repository(_memory)
    memory_repo.data = packages

    config.remove_override("packages_path")
    config.remove_override("allow_unversioned_packages")


def _git_clone_packages():
    for repo in _pkg_repos:
        # TODO: checkout latest
        git.clone(
            url=repo["url"],
            dst=os.path.join(_root, "downloads", repo["name"]),
            branch=repo.get("branch"),
        )


def _bind(name):
    from rez.packages import get_latest_package_from_string

    pkg = get_latest_package_from_string(name, paths=_state["packages_path"])
    if pkg is None:
        subprocess.check_call(_state["bind_cmd"] + [name])
        _clear_repo_cache()


if __name__ == "__main__":
    # TODO: ensure vcs plugin "kit" is loaded on package release
    # TODO: This deploy script requires to be in rez venv
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

    os.environ["REZ_CONFIG_FILE"] = os.pathsep.join(
        [os.path.join(_root, "rezconfig.py")] +
        os.getenv("REZ_CONFIG_FILE", "").split(os.pathsep)
    )

    if opt.list:
        print_developer_packages(opt.packages)
        sys.exit(0)

    if opt.packages:
        set_release(opt.release)
        if deploy_packages(opt.packages, opt.yes):
            print("=" * 30)
            print("SUCCESS!\n")

    else:
        print("Please name at least one package to deploy. Use --list to "
              "view available packages.")
