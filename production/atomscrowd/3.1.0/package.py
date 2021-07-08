
name = "atomscrowd"

version = "3.1.0-m1"

_data = {
    # Allzpark
    "label": "AtomsCrowd",
    "icon": "{root}/logo.png"
}

requires = [
    "~arnold_core-5.2.2.1|5.4.0.0",
    "~redshift-2.6.41",
    "atomscrowd_base-1",
]

variants = [
    ["platform-*", "maya"],
]

private_build_requires = ["rezutil-1"]
build_command = "python -m rezutil build {root} --use-zip"
