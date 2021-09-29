
name = "atomsvfx"

version = "4.4.0-m1"

_data = {
    # Allzpark
    "label": "AtomsVFX",
    "icon": "{root}/logo.png"
}

requires = [
    "~maya-2018+<2023",
    "~arnold_core-5.1.1.1+<=6.2.1.1_",
    "~redshift-3.0.36|3.0.44|3.0.45|3.0.49|3.0.50",
    "atomsbase-1",
    "!atomscrowd",
]

variants = [
    ["platform-*", "maya"],
    ["platform-*", "houdini-18.5.408"],
    ["platform-*", "houdini-18.5.499"],
    ["platform-*", "houdini-18.5.532"],
    ["platform-*", "houdini-18.5.563"],
    ["platform-*", "houdini-18.5.596"],
    ["platform-*", "houdini-18.5.633"],  # py3
    ["platform-*", "houdini-18.5.672"],  # py3
    ["platform-*", "houdini-18.5.696"],  # py3
]

private_build_requires = ["rezutil-1"]
build_command = "python -m rezutil build {root} --use-zip"
