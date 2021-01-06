
# `parser` var will be given by custom build system
parser = globals()["parser"]


parser.add_argument(
    "--name",
    required=True,
    type=str,
    help="Package name"
)
parser.add_argument(
    "--version",
    required=True,
    type=str,
    help="Package version"
)
parser.add_argument(
    "--requires",
    nargs="+",
    help="Package requirements"
)
parser.add_argument(
    "--tools",
    nargs="+",
    help="Package bin tools"
)
