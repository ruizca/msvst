import os
from subprocess import call

from setuptools import setup
from setuptools.command.install import install


class CustomInstall(install, object):
    """Custom handler for the 'install' command."""

    def run(self):
        os.environ["CC"] = "gcc"
        os.environ["CXX"] = "g++"
        os.makedirs("build", exist_ok=True)
        call(["cmake", "-H.", "-Bbuild"])
        call(["make", "-Cbuild"])
        call(["make", "-Cbuild", "install"])
        super(CustomInstall, self).run()

setup(
    name="msvst",
    version="1.0",
    description="lol",
    packages=["msvst"],
    package_dir={"msvst": "msvst/"},
    package_data={"msvst": ["bin/*"]},
    cmdclass={"install": CustomInstall},
)
