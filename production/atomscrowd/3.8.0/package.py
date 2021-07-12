
name = "atomscrowd"

version = "3.8.0-m1"

_data = {
    # Allzpark
    "label": "AtomsCrowd",
    "icon": "{root}/logo.png"
}

requires = [
    "~maya-2017+<=2020",
    "~arnold_core-5.1.1.1+<=6.1.0.0",
    "~redshift-2.6.19|2.6.41|2.6.51",
    "atomsbase-1",
    "!atomsvfx",
]

variants = [
    ["platform-*", "maya"],
    ["platform-*", "houdini-18.0.597"],
    ["platform-*", "houdini-18.5.351"],
]

private_build_requires = ["rezutil-1"]
build_command = "python -m rezutil build {root} --use-zip"
