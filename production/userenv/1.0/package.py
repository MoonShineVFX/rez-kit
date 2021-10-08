
name = "userenv"

version = "1.0-m1"

description = """Appending cherry-picked env from parent process

Artist may need additional env variables to pick up personal tooling for
their own work.

Although we could address this by registering those env variables into
`rezconfig.parent_variables`, but we'd like to always appending those
into resolved context. Hence this package.

To use this package, other than requesting it explicitly, adding it into
`rezconfig.implicit_packages` is a good fit as well. Like so:

```python
# rezconfig.py
implicit_packages = ModifyList(append=[
    "userenv",
])
```

Env vars that will be picked:

* HOUDINI_PACKAGE_DIR

"""

build_command = False


def post_commands():
    import os
    env = globals()["env"]
    resolve = globals()["resolve"]

    user_env = list()

    if "houdini" in resolve:
        user_env += [
            "HOUDINI_PACKAGE_DIR",
        ]

    for key in [k for k in user_env if k in os.environ]:
        env[key].append(os.environ[key])
