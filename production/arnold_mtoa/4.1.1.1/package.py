
name = "arnold_mtoa"

version = "4.1.1.1-m1"

_data = {
    # Allzpark
    "label": "MtoA",
    "icon": "{root}/arnold.ico"
}

requires = [
    "arnold_core-6.1.0.1",
]

variants = [
    ["platform-*", "maya-2018"],
    # ["platform-*", "maya-2019"],
    ["platform-*", "maya-2020"],
]

tools = [
    "kick",
    "oslc",
    "oslinfo",
    "oiiotool",
    "maketx",
    "noice",
]


private_build_requires = ["rezutil-1"]
build_command = "python -m rezutil build {root} --use-zip"
