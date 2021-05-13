"""
This script is a workaround for opt-out unwanted local Maya.env setup.

For Maya 2020+, there is an environment variable called `MAYA_ENV_DIR` which
can be set to read the Maya.env file from a custom location instead of from
the MAYA_APP_DIR location (default behavior).

The following setup will be excluded :
* Local installed Redshift

"""
import os


PREFIX_TO_EXCLUDE = [
    "C:/ProgramData/Redshift",
]
TO_FILTER = [
    "PATH",
    "PYTHONPATH",
    "MAYA_SCRIPT_PATH",
    "MAYA_PLUG_IN_PATH",
    "MAYA_RENDER_DESC_PATH",
    "MAYA_CUSTOM_TEMPLATE_PATH",
    "XBMLANGPATH",

    "REDSHIFT_COREDATAPATH",
    "REDSHIFT_PLUG_IN_PATH",
    "REDSHIFT_SCRIPT_PATH",
    "REDSHIFT_XBMLANGPATH",
    "REDSHIFT_RENDER_DESC_PATH",
    "REDSHIFT_CUSTOM_TEMPLATE_PATH",
    "REDSHIFT_MAYAEXTENSIONSPATH",
    "REDSHIFT_PROCEDURALSPATH",
]

print("Cleaning environment variables..\n")

_exclude = [os.path.normpath(p).lower() for p in PREFIX_TO_EXCLUDE]
for key in TO_FILTER:
    if key not in os.environ:
        continue

    clean = list()
    for p in os.environ[key].split(os.path.pathsep):
        if any(os.path.normpath(p).lower().startswith(e) for e in _exclude):
            continue
        clean.append(p)

    if clean:
        os.environ[key] = os.path.pathsep.join(clean)
    else:
        del os.environ[key]
