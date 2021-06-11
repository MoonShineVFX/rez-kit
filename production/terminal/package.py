
name = "terminal"

version = "0.1.0-m1"

tools = ["terminal"]

build_command = False


def commands():
    alias("terminal", "start cmd.exe")
