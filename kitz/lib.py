
import os
import stat
import shutil
import contextlib


def confirm(msg):
    try:
        _input = raw_input
    except NameError:
        _input = input

    try:
        reply = _input(msg).lower().rstrip()
        return reply in ("", "y", "yes", "ok")
    except EOFError:
        return True  # On just hitting enter
    except KeyboardInterrupt:
        return False


@contextlib.contextmanager
def working_dir(path):
    cwd = os.getcwd()
    if not os.path.isdir(path):
        os.makedirs(path)
    try:
        os.chdir(path)
        yield
    finally:
        os.chdir(cwd)


def clean(path):
    def del_rw(action, name, exc):
        # handling read-only files, e.g. in .git
        os.chmod(name, stat.S_IWRITE)
        os.remove(name)

    shutil.rmtree(path, onerror=del_rw)
