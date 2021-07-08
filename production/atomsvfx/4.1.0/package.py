
name = "atomsvfx"

version = "4.0.0-m1"

_data = {
    # Allzpark
    "label": "AtomsVFX",
    "icon": "{root}/logo.png"
}

requires = [
    "~arnold_core-5.2.2.1|5.4.0.0|6.0.4.0",
    "~redshift-2.6.41|2.6.51",
    "atomscrowd_base-1",
]

variants = [
    ["platform-*", "maya"],
    # ["platform-*", "houdini-18.5.408"],
    # ["platform-*", "houdini-18.5.499"],
    ["platform-*", "houdini-18.5.532"],
    # ["platform-*", "houdini-18.5.563"],
    # ["platform-*", "houdini-18.5.596"],
]

private_build_requires = ["rezutil-1"]
build_command = "python -m rezutil build {root} --use-zip"
