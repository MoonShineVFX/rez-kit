
name = "arnold_mtoa"

version = "4.2.2-m1"

_data = {
    # Allzpark
    "label": "MtoA",
    "icon": "{root}/arnold.ico"
}

requires = [
    "arnold_core-6.2.1.0",
]

variants = [
    # ["platform-*", "maya-2019"],
    ["platform-*", "maya-2020"],
    ["platform-*", "maya-2022"],
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
