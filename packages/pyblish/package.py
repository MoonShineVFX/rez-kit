
name = "pyblish"

description = "Test-driven content creation, see http://pyblish.com"

version = "1.8.7-m1"


authors = [
   "Marcus Ottosson",
   "Toke Jepsen",
   "Jeremy Retailleau",
   "Paul Schweizer",
   "Philip Scadding",
   "Roy Nieterau",
   "aardschok",
   "Alan Fregtman",
   "Lars van der Bijl",
   "antirotor",
   "iLLiCiTiT",
   "p4vv37",
   "David Lai",
   "Ian Wootten",
   "Jimmy-Lee Boisvert",
   "The Gitter Badger",
   "davidpower",
   "marcus",
   "Jed Frechette",
   "LIJU",
   "davidlatwe",
   "wijnand",
]


tools = [
]

requires = [
    "python",
]


private_build_requires = ["rezutil-1"]
build_command = "python {root}/rezbuild.py {install}"


def commands():
    env = globals()["env"]
    env.PYTHONPATH.prepend("{root}/payload/lib")
