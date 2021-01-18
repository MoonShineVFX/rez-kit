
name = "libjpeg_turbo"

version = "1.5.1-m1"

variants = [
    ["arch-*", "os-*"],
]

build_requires = [
    "rezutil-1+",
    "cmake-2.8+",
    "nasm-2.14+",
]
build_command = "python {root}/rezbuild.py {install}"


def commands():
    env = globals()["env"]

    env.PATH.append("{root}/bin")
    env.PATH.append("{root}/lib")
    env.JPEG_LIBRARIES = "{root}"
