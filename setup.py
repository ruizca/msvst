import os
from pathlib import Path
from subprocess import call

from setuptools import setup
from setuptools.command.build_py import build_py


class CustomBuild(build_py):
    """Custom handler for the 'build_py' command."""

    def run(self):
        os.environ["CC"] = "gcc"
        os.environ["CXX"] = "g++"
        os.makedirs("build", exist_ok=True)
        call(["cmake", "-H.", "-Bbuild"])
        call(["make", "-Cbuild"])
        call(["make", "-Cbuild", "install"])
        super(CustomBuild, self).run()

this_directory = Path(__file__).parent
long_description = (this_directory / "README.md").read_text()

setup(
    name="msvst",
    version="1.0",
    license='CeCILL',
    description='Multi-Scale Variance Stabilization Transform',
    long_description=long_description,
    long_description_content_type='text/markdown',
    author='Angel Ruiz',
    author_email='angel.ruizca@gmail.com',
    url="https://github.com/ruizca/msvst",
    packages=["msvst"],
    package_dir={"msvst": "msvst/"},
    package_data={"msvst": ["bin/*"]},
    include_package_data=True,
    cmdclass={"build_py": CustomBuild},
    classifiers=[
        "Intended Audience :: Science/Research",
        "Topic :: Scientific/Engineering :: Astronomy",
        "Programming Language :: Python :: 3",
        "Operating System :: POSIX :: Linux",
    ],
)
