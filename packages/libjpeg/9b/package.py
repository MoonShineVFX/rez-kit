# NOTE:
#   On Windows, this is actually `libjpeg-turbo`, NOT `libjpeg`.
#   This is for building Pixar USD.
name = "libjpeg"

version = "9b-m1"

variants = [
    ["arch", "os"],
]

build_requires = [
    "rezutil-1+",
    "cmake-3.2+",
]
build_command = "python {root}/rezbuild.py {install}"


def commands():
    env = globals()["env"]

    env.PATH.append("{root}/bin")
    env.PATH.append("{root}/lib")
    env.JPEG_LIBRARIES = "{root}"
