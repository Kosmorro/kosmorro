# ![Kosmorro](kosmorrolib/assets/png/kosmorro-logo.png)
[![Coverage Status](https://coveralls.io/repos/github/Kosmorro/kosmorro/badge.svg?branch=master)](https://coveralls.io/github/Kosmorro/kosmorro?branch=master) [![Version on PyPI](https://img.shields.io/pypi/v/kosmorro)](https://pypi.org/project/kosmorro) [![Discord](https://img.shields.io/discord/650237632533757965?logo=discord&label=%23kosmorro)](https://discord.gg/TVX4MSKGaa)

A program that calculates your astronomical ephemerides!

## Installation

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
If you don't have it, install [HomeBrew](https://formulae.brew.sh), then install Python 3: `brew install python`.

This will install Python 3 and its PIP on your system. Note that their executables are called `python3` and `pip3`.
Now, you can install Kosmorro with your PIP: `pip3 install kosmorro`.

#### Windows

Kosmorro being at an early-stage development, Windows is not supported officially for now.

#### Docker

Get the official Kosmorro Docker image by running `docker pull kosmorro/kosmorro`.

Now that you have the image, you can run it with `docker run -it kosmorro`.
Run Kosmorro by executing `kosmorro` in the container.

You can also run the image with the command: `docker run kosmorro kosmorro [args]`.

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
Before you use this feature, make sure you have installed a LaTeX distribution:

- **Linux:** install TeXLive through your packages manager. Kosmorro just needs the minimal installation, you don't need any extension.  
  Note: **on Ubuntu 20.04+**, you will also need the `texlive-latex-extra` package.
- **macOS**: install basic version of [MacTeX](https://www.tug.org/mactex/):
    - from the official website, choose the _smaller download_
    - with Brew: `brew install basictex`

These dependencies are not installed by default, because they take a lot of place and are not necessary if you are not interested in generating PDF files.
