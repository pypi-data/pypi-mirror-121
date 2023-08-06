import os
import shutil
import subprocess
import sys

from setuptools import (
    Command,
    find_packages,
    setup,
)
from setuptools.command.install_lib import install_lib

__version__ = "0.2.0"

sys.path.insert(0, "lib/python")
from jpipe.jp.main import (
    __description__,
)

sys.path.remove("lib/python")

__project__ = "jpipe"
__author__ = "Zac Medico"
__email__ = "<zmedico@gmail.com>"
__classifiers__ = (
    "License :: OSI Approved :: Apache Software License",
    "Operating System :: POSIX",
    "Programming Language :: Python :: 3",
    "Programming Language :: Unix Shell",
)
__copyright__ = "Copyright 2021 Zac Medico"
__license__ = "Apache-2.0"
__url__ = "https://github.com/pipebus/jpipe"
__project_urls__ = (("Bug Tracker", "https://github.com/pipebus/jpipe/issues"),)


class PyTest(Command):
    user_options = [
        ("match=", "k", "Run only tests that match the provided expressions")
    ]

    def initialize_options(self):
        self.match = None

    def finalize_options(self):
        pass

    def run(self):
        testpath = "./test"
        pytest_exe = shutil.which("py.test")
        if pytest_exe is not None:
            test_cmd = (
                [
                    pytest_exe,
                    "-s",
                    "-v",
                    testpath,
                    "--cov-report=xml",
                    "--cov-report=term-missing",
                ]
                + (["-k", self.match] if self.match else [])
                + ["--cov=jpipe"]
            )
        else:
            test_cmd = ["python", "test/test_jpipe.py"]
        subprocess.check_call(test_cmd)


def version_subst(filename):
    with open(filename, "rt") as f:
        content = f.read()
        if "VERSION" in content:
            content = content.replace("VERSION", __version__)
            with open(filename, "wt") as f:
                f.write(content)


class x_install_lib(install_lib):
    def install(self):
        ret = install_lib.install(self)
        extra_python_dir = os.path.join(self.install_dir, "python")
        if os.path.isdir(extra_python_dir):
            shutil.rmtree(extra_python_dir)

        for dirpath, _dirnames, filenames in os.walk(self.install_dir):
            if "__init__.py" in filenames:
                for filename in filenames:
                    if filename.endswith(".py"):
                        version_subst(os.path.join(dirpath, filename))

        return ret


with open(os.path.join(os.path.dirname(__file__), "README.md"), "rt") as f:
    long_description = f.read()


setup(
    name=__project__,
    version=__version__,
    description=__description__,
    long_description=long_description,
    long_description_content_type="text/markdown",
    author=__author__,
    author_email=__email__,
    url=__url__,
    project_urls=dict(__project_urls__),
    classifiers=list(__classifiers__),
    cmdclass={
        "install_lib": x_install_lib,
        "test": PyTest,
    },
    install_requires=["jmespath"],
    package_dir={"": "lib/python"},
    packages=find_packages(where="./lib/python"),
    entry_points={
        "console_scripts": [
            "jpipe = jpipe.cmd.main:jpipe_main",
            "jp = jpipe.jp.main:jp_main",
            "jpp = jpipe.jpp.main:jpp_main",
            "jpipe-jp = jpipe.jp.main:jp_main",
            "jpipe-jpp = jpipe.jpp.main:jpp_main",
        ]
    },
    python_requires=">=3.6",
)
