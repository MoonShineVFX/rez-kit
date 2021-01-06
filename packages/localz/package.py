
import subprocess
early = globals()["early"]


name = "localz"

version = "0.4.2-m1"

description = "Package localisation for Rez"


@early()
def authors():
    name_list = subprocess.check_output(
        ["git", "shortlog", "-sn"]
    ).decode()
    return [
        n.strip().split("\t", 1)[-1]
        for n in name_list.strip().split("\n")
    ]


requires = [
    "python-2.7+,<4",
    "rez-2.29+",
]

tools = [
    "listen",
    "localise",
    "localize",
]

build_command = "python {root}/install.py"


def commands():
    env = globals()["env"]

    env.PATH.prepend("{root}/bin")
    env.PYTHONPATH.prepend("{root}/python")
