
name = "maya_devkit"

version = "2020.2-m1"

description = "Autodesk Maya Devkit"

requires = [
    "maya-2020",
    "~qt-5.12.5",
]

variants = [
    ["platform-*"]
]


private_build_requires = ["rezutil-1"]
build_command = "python -m rezutil build {root} --use-zip"


def commands():
    env = globals()["env"]
  
    # Note that the devkitBase folder is: {root}/devkitBase 
    env.MAYA_DEVKIT_LOCATION = "{root}/devkitBase"
    env.MAYA_DEVKIT_INC_DIR = "{root}/devkitBase/include"
