# ![Kosmorro](https://raw.githubusercontent.com/Kosmorro/logos/main/png/kosmorro-logo-grey.png)
[![Coverage Status](https://coveralls.io/repos/github/Kosmorro/kosmorro/badge.svg?branch=master)](https://coveralls.io/github/Kosmorro/kosmorro?branch=master) [![Version on PyPI](https://img.shields.io/pypi/v/kosmorro)](https://pypi.org/project/kosmorro) [![Packaging status](https://repology.org/badge/tiny-repos/kosmorro.svg)](https://repology.org/project/kosmorro/versions) [![Docker Pulls](https://img.shields.io/docker/pulls/kosmorro/kosmorro)](https://hub.docker.com/r/kosmorro/kosmorro) [![Help translating Kosmorro!](https://hosted.weblate.org/widgets/kosmorro/-/cli/svg-badge.svg)](https://hosted.weblate.org/engage/kosmorro/)

A program that calculates your astronomical ephemerides!

## Installation

### Production environment

If you want to give a try to Kosmorro, head to [its official download page](https://kosmorro.space/cli/download/) and follow the instructions that correspond to your operating system.

### Development environment

Before you run Kosmorro in your development environment, check you have installed these programs on your system:

- Python ≥ 3.7.0 (needed run Kosmorro)
- PIP3 (needed for package management, usually installed among with Python 3)
- [Pipenv](https://pypi.org/project/pipenv/) (needed to manage the virtual environment)

Clone this repository and run `pipenv sync` to install all the dependencies.
Then, run Kosmorro by invoking `pipenv run python kosmorro`.

For comfort, you may want to invoke `pipenv shell` first and then just `python kosmoro`.

## Using Kosmorro

Using Kosmorro is as simple as invoking `kosmorro` in your terminal!

By default, it will give you the current Moon phase and, if any, the events that will occur today.
To get the rise, culmination and set of the objects of the Solar system, you will need to give it your position on Earth: get your current coordinates (with [OpenStreetMap](https://www.openstreetmap.org) for instance), and give them to Kosmorro by invoking it with the following parameters: `--latitude=X --longitude=Y` (replace `X` by the latitude and `Y` by the longitude).

Kosmorro has a lot of available options. To get a list of them, run `kosmorro --help`, or read its manual with `man kosmorro`.

Note: the first time it runs, Kosmorro will download some important files needed to make the computations. They are stored in a cache folder named `.kosmorro-cache` located in your home directory (`/home/<username>` on Linux, `/Users/<username>` on macOS).

### Exporting to PDF

Kosmorro can export the computation results to PDF files, but this feature requires first that you install some additional dependencies.
You can find documentation about this on [Kosmorro's website](https://kosmorro.space/cli/generate-pdf/).

## Help translating Kosmorro!

Kosmorro is translated on [Weblate](https://hosted.weblate.org/engage/kosmorro/), a popular free platform for crowd-sourced internationalization.
If you speak a language that is not supported yet, feel free to contribute!

![Translation state per language](https://hosted.weblate.org/widgets/kosmorro/-/cli/multi-auto.svg)
