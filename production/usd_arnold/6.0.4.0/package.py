
name = "usd_arnold"

version = "6.0.4.0-m1"

requires = [
    "arnold_core-6.0.4.0",
]

variants = [
    ["platform-*", "usd-20.05"],
    ["platform-*", "usd-20.08"],
    # ["platform-*", "houdini-18.0.532"],
]

build_requires = [
    "rezutil-1+",
    "cmake-3.2+",
    "boost",
    "tbb",
    "python-2.7",
    "arnold_sdk-6.0.4.0",
]
build_command = "python {root}/rezbuild.py {install}"


def commands():
    global env
    global request

    env.PATH.prepend("{root}/bin")
    env.LD_LIBRARY_PATH.prepend('{root}/lib/')  # unix
    env.PATH.prepend("{root}/lib")              # windows
    
    env.ARNOLD_PLUGIN_PATH.append("{root}/plugin")      # todo: not needed?
    env.ARNOLD_PLUGIN_PATH.append("{root}/procedural")
    env.PATH.append("{root}/procedural")
    
    env.PYTHONPATH.append("{root}/lib/python")
    env.PXR_PLUGINPATH_NAME.append("{root}/plugin")
    
    # todo: is this needed for mtoa?
    if "maya" in request:
        env.MTOA_EXTENSIONS_PATH.append("{root}/plugin")
