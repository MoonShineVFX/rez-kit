
name = "nasm"

version = "2.14.02-m1"

description = "A cross-platform x86 assembler with an Intel-like syntax"

url = "https://github.com/netwide-assembler/nasm"
download_bin = "https://www.nasm.us/pub/nasm/releasebuilds/2.14.02/win64"

build_command = False


def commands():
    env = globals()["env"]
    env.PATH.append("c:/nasm-2.14.02")
