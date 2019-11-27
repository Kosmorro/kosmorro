# ![Kosmorro](assets/png/kosmorro-logo.png)
[![Language grade: Python](https://img.shields.io/lgtm/grade/python/g/Deuchnord/kosmorro.svg?logo=lgtm&logoWidth=18)](https://lgtm.com/projects/g/Deuchnord/kosmorro/context:python) [![codecov](https://codecov.io/gh/Deuchnord/kosmorro/branch/master/graph/badge.svg)](https://codecov.io/gh/Deuchnord/kosmorro) [![Version on PyPI](https://img.shields.io/pypi/v/kosmorro)](https://pypi.org/project/kosmorro)

## About the project

Kosmorro is a software that allows you to compute the ephemeris for a date, a month or a year.

## Installation

### Requirements

Kosmorro requires the following software to work:

- Python ≥ 3.5.0
- PIP

### Production environment

Keep in mind that Kosmorro is still in alpha development stage and is not considered as stable.

#### Linux

##### Arch Linux, Manjaro…

Kosmorro is available [in the AUR](https://aur.archlinux.org/packages/kosmorro).

##### Other distributions

Kosmorro is available [on PyPI](https://pypi.org/project/kosmorro/), a repository dedicated to Python.
First, install `python-pip` on your system and invoke the following command: `pip install kosmorro`.

#### macOS

Currently, macOS does not provide Python 3, so you will first have to install it.
If you don't have it, first install [HomeBrew](https://formulae.brew.sh), then install Python 3: `brew install python`.

This will install Python 3 and its PIP on your system. Note that their executables are called `python3` and `pip3`.
Now, you can install Kosmorro with your PIP: `pip3 install kosmorro`.

#### Windows

Kosmorro being at an early-stage development, Windows is not supported officially for now.

### Development environment

First, install [Pipenv](https://pypi.org/project/pipenv/).

Clone this repository and run `pipenv sync` to install all the dependencies.
Then, run Kosmorro by invoking `pipenv run python kosmorro`.

For comfort, you may want to invoke `pipenv shell` first and then just `python kosmoro`.

## Running Kosmorro

Using Kosmorro is as simple as invoking `kosmorro` in your terminal!

By default, it will compute and display the ephemerides for the current day, for the cordinates `(0;0)`.
To set your position on Earth, get your coordinates (with [OpenStreetMap](https://www.openstreetmap.org) for instance), and give them to Kosmorro by invoking it with the following parameters: `--latitude=X --longitude=Y` (replace `X` by the latitude and `Y` by the longitude).

Kosmorro has a lot of available options. To get a list of them, run `kosmorro --help`.

Note: the first time it runs, Kosmorro will download some important files needed to make the computations. They are stored in a cache folder named `.kosmorro-cache` located in your home directory (`/home/<username>` on Linux, `/Users/<username>` on macOS).

