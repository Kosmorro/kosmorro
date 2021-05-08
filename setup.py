#!/usr/bin/env python3

#    Kosmorro - Compute The Next Ephemerides
#    Copyright (C) 2019  Jérôme Deuchnord <jerome@deuchnord.fr>
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as
#    published by the Free Software Foundation, either version 3 of the
#    License, or (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU Affero General Public License for more details.
#
#    You should have received a copy of the GNU Affero General Public License
#    along with this program.  If not, see <https://www.gnu.org/licenses/>.

import pathlib
from setuptools import setup, find_packages

from _kosmorro.__version__ import __version__

HERE = pathlib.Path(__file__).parent
README = (HERE / "README.md").read_text()

setup(
    name="kosmorro",
    version=__version__,
    author="Jérôme Deuchnord",
    author_email="jerome@deuchnord.fr",
    url="http://kosmorro.space",
    license="AGPL-3.0",
    description="A program that computes the ephemerides.",
    long_description=README,
    long_description_content_type="text/markdown",
    keywords="kosmorro astronomy ephemerides ephemeris",
    packages=find_packages(),
    scripts=["kosmorro"],
    include_package_data=True,
    data_files=[
        ("man/man1", ["manpage/kosmorro.1"]),
        ("man/man7", ["manpage/kosmorro.7"]),
    ],
    install_requires=[
        "kosmorrolib",
        "tabulate",
        "termcolor",
        "python-dateutil",
    ],
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Operating System :: POSIX :: Linux",
        "Operating System :: MacOS :: MacOS X",
        "Environment :: Console",
        "Topic :: Scientific/Engineering :: Astronomy",
    ],
    python_requires=">=3.7",
)
