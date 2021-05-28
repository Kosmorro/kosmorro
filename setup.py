#!/usr/bin/env python3

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
    license="CeCILL-v2.1",
    description="A program to compute the ephemerides.",
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
