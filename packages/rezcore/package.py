
name = "rezcore"

description = "Find and enter Rez's virtual env, use with caution."

version = "1.0.0"

build_command = False


def commands():
    import os
    from rez.system import system
    env = globals()["env"]

    location = system.rez_bin_path

    if location is None and "REZ_USED" in os.environ:
        # Search in resolved context
        if system.platform == "windows":
            bin_dir = "Scripts"
            feature = {"activate", "rez", "pip.exe", "python.exe"}
        else:
            bin_dir = "bin"
            feature = {"activate", "rez", "pip", "python"}

        def up(path):
            return os.path.dirname(path)

        current = os.path.dirname(os.environ["REZ_USED"])
        while True:
            if bin_dir not in os.listdir(current):
                parent_dir = up(current)
                if current == parent_dir:
                    break  # reached to root
                current = parent_dir
            else:
                found = os.path.join(current, bin_dir)
                content = set(os.listdir(found))
                if content.issuperset(feature):
                    location = os.path.join(found, "rez")
                    break

    if location is None:
        raise Exception("Rez bin dir not found.")

    venv_path = os.path.dirname(location)

    env.PYTHONHOME.unset()
    env.PYTHONPATH = ""
    env.PATH.prepend(venv_path)
    env.REZ_CORE_BIN_PATH = location
