
name = "doxygen"

version = "1.8.20-m1"

description = "Generate documentation from source code"

download_bin = "http://doxygen.nl/files/doxygen-1.8.20-setup.exe"

build_command = False


def commands():
    env = globals()["env"]
    env.PATH.append("c:/Program Files/doxygen/bin")
