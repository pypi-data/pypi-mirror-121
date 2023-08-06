##
#   Copyright (c) 2021 Valentin Weber
#
#   This file is part of the software steam-scheduled-download-killer.
#
#   The software is licensed under the European Union Public License
#   (EUPL) version 1.2 or later. You should have received a copy of
#   the english license text with the software. For your rights and
#   obligations under this license refer to the file LICENSE or visit
#   https://joinup.ec.europa.eu/community/eupl/og_page/eupl to view
#   official translations of the licence in another language of the EU.
##

"""Setup script."""

import subprocess  # nosec
from os import path
from types import FunctionType
from typing import List, TextIO

from setuptools import find_packages, setup

from ssdk.cli import SSDK_LIB, SSDK_MAIN, lib, ssdk

HEREDIR = path.abspath(path.dirname(__file__))

PROG = "steam-scheduled-download-killer"
DESC = "Set update priority for all Steam games to avoid scheduled downloads."
VERSION = "0.0.1"
GITHUB = "https://github.com/vlntnwbr/ssdk"


def get_entry_point(name: str, function: FunctionType) -> str:
    """Return string for a named function entry point for setuptools."""
    return "{}={}:{}".format(
        name, function.__module__, function.__name__
    )


def open_local(filename: str, mode: str = "r") -> TextIO:
    """Open file in this directory."""
    return open(path.join(HEREDIR, filename), mode, encoding="utf-8")


def execute_command(args: List[str]) -> List[str]:
    """Execute external command and return stdout as list of strings."""
    try:
        process = subprocess.run(  # nosec
            args,
            capture_output=True,
            check=True,
            text=True
        )
        return [line.strip() for line in process.stdout.splitlines()]
    except subprocess.CalledProcessError:
        return []


if __name__ == '__main__':
    README = open_local("README.md").read()
    setup(
        name=PROG,
        description=DESC,
        long_description=README,
        long_description_content_type="text/markdown",
        version=VERSION,
        packages=find_packages(),
        include_package_data=True,
        platforms="windows",
        python_requires=">=3.9",
        license="EUPL",
        url=GITHUB,
        author="Valentin Weber",
        author_email="dev@vweber.eu",
        maintainer="Valentin Weber",
        maintainer_email="dev@vweber.eu",
        project_urls={"Bug Tracker": GITHUB + "/issues?q=label%3bug"},
        entry_points={'console_scripts': [
            get_entry_point(SSDK_MAIN, ssdk.main),
            get_entry_point(SSDK_LIB, lib.main)
        ]},
        classifiers=[
            "Development Status :: 1 - Planning",
            "Environment :: Console",
            "Intended Audience :: End Users/Desktop",
            "Intended Audience :: Other Audience",
            "License :: OSI Approved :: European Union Public Licence 1.2 (EUPL 1.2)",  # noqa pylint: disable=line-too-long
            "Operating System :: Microsoft :: Windows :: Windows 10",
            "Programming Language :: Python :: 3 :: Only",
            "Topic :: Desktop Environment :: File Managers",
            "Topic :: Games/Entertainment",
            "Topic :: Utilities"
        ]
    )
