
name = "python_dotenv"

description = "Add .env support to your django/flask apps in " \
              "development and deployments"

version = "0.14.0-m1"

requires = []

variants = []

pip_packages = [
    "python_dotenv==0.14.0",
]

private_build_requires = ["pipz"]
build_command = "install %s --bundle" % " ".join(pip_packages)


def commands():
    env = globals()["env"]

    env.PATH.prepend("{root}/bin")
    env.PYTHONPATH.prepend("{root}/python")
