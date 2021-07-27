
name = "atomscrowd"

version = "3.8.1-m2"

_data = {
    # Allzpark
    "label": "AtomsCrowd",
    "icon": "{root}/logo.png"
}

requires = [
    "~maya-2017+<2021",
    "~arnold_core-5.1.1.1+<=6.1.0.0_",
    "~redshift-2.6.19|2.6.41|2.6.51|3.0.36|3.0.44",
    # NOTE: redshift-3 were custom builds kindly provided by Atoms support
    #   and only for maya-2020.
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
