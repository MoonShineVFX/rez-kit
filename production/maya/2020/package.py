
name = "maya"

version = "2020-m2"

description = "Autodesk Maya 2020"

_data = {
    # Allzpark
    "label": "Maya",
    "icon": "{root}/resources/mayaico.png"
}

requires = [
    "!PySide2",
    "~maya_devkit==2020",
]


tools = [
    "maya",
]


private_build_requires = ["rezutil-1"]
build_command = "python -m rezutil build {root}"


def pre_commands():
    env = globals()["env"]
    system = globals()["system"]

    env.MAYA_VERSION = str(env.REZ_MAYA_VERSION).rsplit("-m", 1)[0]

    if system.platform == "windows":
        env.MAYA_LOCATION = "C:/Program Files/Autodesk/Maya{env.MAYA_VERSION}"

    elif system.platform == "linux":
        env.MAYA_LOCATION = "/usr/autodesk/maya{env.MAYA_VERSION}"

    elif system.platform == "osx":
        env.MAYA_LOCATION = "/Applications/Autodesk/maya{env.MAYA_VERSION}" \
                            "/Maya.app/Contents"


def commands():
    env = globals()["env"]
    system = globals()["system"]

    env.PATH.append("{env.MAYA_LOCATION}/bin")

    if system.platform == "windows":
        env.PATH.append("C:/Program Files/Common Files/Autodesk Shared/")
        env.PATH.append("C:/Program Files (x86)/Autodesk/Backburner/")

    elif system.platform == "linux":
        pass

    elif system.platform == "osx":
        env.DYLD_LIBRARY_PATH = "{env.MAYA_LOCATION}/MacOS"

    # clean Maya.env
    env.MAYA_ENV_DIR = "{root}/resources"

    # Override some Maya default settings (optimization)
    # todo: These might need to be moved out to be left to company specific choices
    env.MAYA_DISABLE_CLIC_IPM = "Yes"
    env.MAYA_DISABLE_CIP = "Yes"
    env.MAYA_DISABLE_CER = "Yes"
    env.PYMEL_SKIP_MEL_INIT = "Yes"
    env.LC_ALL = "C"

    # Enable OpenGL in remote desktop
    env.MAYA_ALLOW_OPENGL_REMOTE_SESSION = "Yes"
