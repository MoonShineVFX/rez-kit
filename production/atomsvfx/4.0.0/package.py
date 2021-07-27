
name = "atomsvfx"

version = "4.0.0-m2"

_data = {
    # Allzpark
    "label": "AtomsVFX",
    "icon": "{root}/logo.png"
}

requires = [
    "~maya-2017+<2021",
    "~arnold_core-5.1.1.1+<=6.2.0.1_",
    "~redshift-3.0.36|3.0.41",
    "atomsbase-1",
    "!atomscrowd",
]

variants = [
    ["platform-*", "maya"],
    ["platform-*", "houdini-18.0.597"],
    ["platform-*", "houdini-18.5.499"],
    ["platform-*", "houdini-18.5.532"],
]

private_build_requires = ["rezutil-1"]
build_command = "python -m rezutil build {root} --use-zip"
