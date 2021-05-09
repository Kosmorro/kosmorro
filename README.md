# ![Kosmorro](kosmorrolib/assets/png/kosmorro-logo.png)
[![Coverage Status](https://coveralls.io/repos/github/Kosmorro/kosmorro/badge.svg?branch=master)](https://coveralls.io/github/Kosmorro/kosmorro?branch=master) [![Version on PyPI](https://img.shields.io/pypi/v/kosmorro)](https://pypi.org/project/kosmorro) [![Discord](https://img.shields.io/discord/650237632533757965?logo=discord&label=%23kosmorro)](https://discord.gg/TVX4MSKGaa) ![Docker Pulls](https://img.shields.io/docker/pulls/kosmorro/kosmorro) [![Help translating Kosmorro!](https://hosted.weblate.org/widgets/kosmorro/-/cli/svg-badge.svg)](https://hosted.weblate.org/engage/kosmorro/)

A program that calculates your astronomical ephemerides!

## Installation

### Production environment

Keep in mind that Kosmorro is still in alpha development stage and is not considered as stable.

#### Available packages

First thing first, check on the badge below (or on [Repology](https://repology.org/project/kosmorro/packages)) if your distribution has a package for Kosmorro.
If possible, prefer these packages, since they provide the best integration with your system, especially the update routine.

[![Packaging status](https://repology.org/badge/vertical-allrepos/kosmorro.svg)](https://repology.org/project/kosmorro/versions)

If it doesn't, then follow the methods ways below.

#### Install from PyPI (Linux, macOS)

> Note: Python 3 and PIP3 is necessary on your machine.
> Please check you have installed it before you install Kosmorro.
> If you need help to install Python 3 and PIP3, please refer to your distribution's manual.

Kosmorro is available [on PyPI](https://pypi.org/project/kosmorro/), a repository dedicated to Python.
To install it, invoke the following command: `pip3 install kosmorro`.

#### Windows

Kosmorro being at an early-stage development, Windows is not supported officially for now.

#### Docker

Kosmorro is available on [Docker Hub](https://hub.docker.com/r/kosmorro/kosmorro)!
You can get it by running `docker pull kosmorro/kosmorro`.

Now that you have the image, you can run it with `docker run -it kosmorro/kosmorro`.
Run Kosmorro by executing `kosmorro` in the container.

You can also run the image with the command: `docker run kosmorro/kosmorro kosmorro [args]`.

Note that for more convenience, you might add the following in your `.bashrc`/`.zshrc`/etc.:

```bash
alias kosmorro="docker run kosmorro/kosmorro kosmorro"
```

##### Image versioning on Docker Hub

By default, running `docker pull kosmorro/kosmorro` will download the `latest` tag by default, which corresponds to the last version of Kosmorro.
If you prefer, you can also force pulling a specific version by specifying it after the `:` character: `docker pull kosmorro/kosmorro:[version]`.

As of version 0.10, five kinds of tags are available:

| Tag | Description | Example
| --- | --- | ---
| `unstable` | the current code in the `master` branch, for testing purpose | `kosmorro/kosmorro:unstable`
| `latest` | the last version (equivalent to not specifying any tag) | `kosmorro/kosmorro:latest`
| `x` | the last version in the `x` major version | `kosmorro/kosmorro:0`: will pull the ![last version in the `0` major branch](https://img.shields.io/docker/v/kosmorro/kosmorro/0?style=flat-square)
| `x.y` | the last version in the `x.y` minor version | `kosmorro/kosmorro:0.10`: will pull the ![last version in the `0` major branch](https://img.shields.io/docker/v/kosmorro/kosmorro/0.10?style=flat-square)
| `x.y.z` | the exact specified version | `kosmorro/kosmorro:0.10.0`

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

## Help translating Kosmorro!

Kosmorro is translated on [Weblate](https://hosted.weblate.org/engage/kosmorro/), a popular free platform for crowd-sourced internationalization.
If you speak a language that is not supported yet, feel free to contribute!

![Translation state per language](https://hosted.weblate.org/widgets/kosmorro/-/cli/multi-auto.svg)
