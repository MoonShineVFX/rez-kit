
name = "atomscrowd"

version = "3.6.0-m1"

_data = {
    # Allzpark
    "label": "AtomsCrowd",
    "icon": "{root}/logo.png"
}

requires = [
    "~maya-2017+<=2020",
    "~arnold_core-5.1.1.1+<=6.0.4.0",
    "~redshift-2.6.19|2.6.41|2.6.51",
    "atomsbase-1",
    "!atomsvfx",
]

variants = [
    ["platform-*", "maya"],
    ["platform-*", "houdini-17.5.460"],
    ["platform-*", "houdini-18.0.566"],
]

private_build_requires = ["rezutil-1"]
build_command = "python -m rezutil build {root} --use-zip"
