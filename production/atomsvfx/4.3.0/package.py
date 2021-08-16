
name = "atomsvfx"

version = "4.3.0-m1"

_data = {
    # Allzpark
    "label": "AtomsVFX",
    "icon": "{root}/logo.png"
}

requires = [
    "~maya-2018+<2023",
    "~arnold_core-5.1.1.1+<=6.2.1.1_",
    "~redshift-3.0.36|3.0.44|3.0.45|3.0.49|3.0.50",
    # NOTE: redshift-3 motion-blur fix were custom builds kindly provided
    #   by Atoms support and only for maya-2020.
    #   (Atoms support ticket ACS-328)
    "atomsbase-1",
    "!atomscrowd",
]

variants = [
    ["platform-*", "maya"],
    # ["platform-*", "houdini-18.5.408"],
    # ["platform-*", "houdini-18.5.499"],
    # ["platform-*", "houdini-18.5.532"],
    # ["platform-*", "houdini-18.5.563"],
    # ["platform-*", "houdini-18.5.596"],
    # ["platform-*", "houdini-18.5.633"],  # py3
]

private_build_requires = ["rezutil-1"]
build_command = "python -m rezutil build {root} --use-zip"
