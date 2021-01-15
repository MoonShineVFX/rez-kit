
name = "tbb"

version = "2020.3-m1"

variants = [
    ["arch", "os"],
]

build_requires = [
    "rezutil-1+",
]
build_command = "python {root}/rezbuild.py {install}"


def commands():
    env = globals()["env"]

    env.PATH.append("{root}/lib")
    env.PATH.append("{root}/bin")

    env.TBB_ROOT_DIR = "{root}"
    env.TBB_INCLUDE_DIR = "{root}/include"
    env.TBB_LIBRARIES = "{root}/lib"
