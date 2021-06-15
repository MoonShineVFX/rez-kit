
name = "python"

description = "Python interpreter provided from virtual env"

uuid = "python.virtualenv"


@early()
def versions():
    from pythonfinder import Finder
    return [
        # e.g. "2.7-venv"
        py.py_version.name + "-venv"
        for py in Finder().find_all_python_versions()
    ]


def commands():
    import os
    import virtualenv
    from pythonfinder import Finder

    finder = Finder()
    python_exec = finder.find_python_version(this.version.major,
                                             minor=this.version.minor)
    if python_exec is None:
        stop("No python installed in system.")

    venv_dir = python_exec.path.parent / "rez.venv"

    args = [
        "--python", str(python_exec.path),
        # "--no-seed",  # no pip, no wheel, no setuptools
        str(venv_dir)
    ]

    # compute venv
    session = virtualenv.session_via_cli(args)

    if not os.path.isdir(str(session.creator.bin_dir)):
        print("\tCreating virtual env..")
        session = virtualenv.cli_run(args)

    env.PATH.prepend(str(session.creator.bin_dir))
