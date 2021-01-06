
name = "vcvars64"

version = "2017-m1"

description = """
Microsoft Visual Studio Developer command prompt

This is a somewhat hacky package that triggers the
Visual Studio Developer command prompt (vcvars64.bat)
and retrieves any environment variables that it sets
so we can apply them with this package environment.

"""

build_command = False

tools = [
    # Missing workload ?
    "cl",
    "cmake"
]


def commands():
    import os
    import subprocess
    env = globals()["env"]

    def collect_environment(cmd):
        # Return the new resulting environment variables from the command
        result = subprocess.check_output("%s & set" % cmd,
                                         universal_newlines=True)

        devenv = {}
        for line in result.splitlines():
            if not line.strip():
                continue
            if line.startswith("*") or line.startswith("_"):
                continue

            if "=" not in line:
                continue

            key, value = line.split("=", 1)

            # In some cases values end with \\ for no reason. Let's force remove it only
            # from those that do not seem to refer to a path (don't have :\ in it, like C:\) 
            if ":\\" not in value and value.endswith("\\"):
                value = value[:-1]

            paths = [x.strip() for x in value.split(os.pathsep) if x.strip()]
            
            # Keep only the paths that are not in the current os.environ to ensure we only
            # get the newly set data from the .bat running through subprocess
            old = set(os.environ.get(key, "").split(os.pathsep))
            if old:
                paths = [p for p in paths if p not in old]
                if not paths:
                    continue
                    
            devenv[key] = os.pathsep.join(paths)

        return devenv

    root = (
        r"C:\Program Files (x86)\Microsoft Visual Studio\2017\Community"
    )

    print("Collect visual studio developer cmd env vars..")
    devenv = collect_environment(root + "/VC/Auxiliary/Build/vcvars64.bat")

    print("Initialize visual studio developer cmd env..")
    for key, paths in sorted(devenv.items()):
        if key.lower() == "path":
            key = "PATH"

        if len(paths.split(os.pathsep)) == 1 and key not in os.environ:
            # Simply set single values as opposed to appending
            # to ensure it's not suddenly prefixed with ;
            env[key] = paths
        else:
            env[key].prepend(paths)
