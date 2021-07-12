
name = "arnold_mtoa"

version = "3.3.0-m2"

_data = {
    # Allzpark
    "label": "MtoA",
    "icon": "{root}/SA.ico"
}

requires = [
    "arnold_core-5.4.0.0",
]

variants = [
    # ["platform-*", "maya-2017"],
    ["platform-*", "maya-2018"],
    # ["platform-*", "maya-2019"],
]

tools = [
    "kick",
    "oslc",
    "oslinfo",
    "maketx",
    "noice",
]


private_build_requires = ["rezutil-1"]
build_command = "python -m rezutil build {root} --use-zip"
