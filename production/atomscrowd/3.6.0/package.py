
name = "atomscrowd"

version = "3.6.0-m1"

_data = {
    # Allzpark
    "label": "AtomsCrowd",
    "icon": "{root}/logo.png"
}

requires = [
    "~arnold_core-5.2.2.1|5.4.0.0|6.0.4.0",
    "~redshift-2.6.41|2.6.51",
    "atomscrowd_base-1",
]

variants = [
    ["platform-*", "maya"],
    ["platform-*", "houdini-17.5.460"],
    # ["platform-*", "houdini-18.0.566"],
]

private_build_requires = ["rezutil-1"]
build_command = "python -m rezutil build {root} --use-zip"
