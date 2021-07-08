
name = "atomscrowd"

version = "2.8.1-m1"

_data = {
    # Allzpark
    "label": "AtomsCrowd",
    "icon": "{root}/logo.png"
}

requires = [
    "~arnold_core-5.2.2.1|5.3.0.2",
    "atomscrowd_base-1",
]

variants = [
    ["platform-*", "maya"],
    # ["platform-*", "houdini-17.5.229"],
]

private_build_requires = ["rezutil-1"]
build_command = "python -m rezutil build {root} --use-zip"
