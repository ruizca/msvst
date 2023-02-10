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
    license='CeCILL',
    description='Multi-Scale Variance Stabilization Transform',
    author='Angel Ruiz',
    author_email='angel.ruizca@gmail.com',
    url="https://github.com/ruizca/msvst",
    packages=["msvst"],
    package_dir={"msvst": "msvst/"},
    package_data={"msvst": ["bin/*"]},
    include_package_data=True,
    cmdclass={"install": CustomInstall},
    classifiers=[
        "Intended Audience :: Science/Research",
        "Topic :: Scientific/Engineering :: Astronomy",
        "Programming Language :: Python :: 3",
        "Operating System :: POSIX :: Linux",
    ],
)
