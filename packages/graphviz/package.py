
name = "graphviz"

version = "2.44.1-m1"

description = "Graphviz - Graph Visualization Software"

url = "https://www.graphviz.org/"

variants = [
    ["platform-*"],
]


private_build_requires = ["rezutil-1"]
build_command = "python {root}/rezbuild.py {install}"


def commands():
    env = globals()["env"]
    env.PATH.append("{root}/payload/bin")
