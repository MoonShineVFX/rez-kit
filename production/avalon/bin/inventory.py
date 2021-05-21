
import os
import sys
from avalon.vendor import toml
from avalon import inventory


def _read(path):
    with open(path) as f:
        return toml.load(f)


_dir = os.path.dirname(__file__)
inventory.DEFAULTS = {
    "config": _read(os.path.join(_dir, ".config.toml")),
    "inventory": _read(os.path.join(_dir, ".inventory.toml"))
}


if __name__ == "__main__":
    try:
        inventory._cli()
    except Exception as e:
        print(e)
        sys.exit(1)
