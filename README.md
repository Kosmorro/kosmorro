# ![Kosmorro](https://github.com/Kosmorro/logos/raw/main/kosmorro/kosmorro-artwork.jpg)
[![Version on PyPI](https://img.shields.io/pypi/v/kosmorro)](https://pypi.org/project/kosmorro) [![Packaging status](https://repology.org/badge/tiny-repos/kosmorro.svg)](https://repology.org/project/kosmorro/versions) [![Help translating Kosmorro!](https://hosted.weblate.org/widgets/kosmorro/-/cli/svg-badge.svg)](https://hosted.weblate.org/engage/kosmorro/)

Kosmorro is a program that calculates your astronomical ephemerides.

## Installation

Installing Kosmorro is documented on [the official website](https://kosmorro.space/cli/download/). Just select your operating system and follow the instructions!

### Development environment

To contribute to Kosmorrolib, you will need [Poetry](https://python-poetry.org), a software to manage the project from development to publishing.

Clone this repository and run `poetry install` to install the dependencies.
And that's all, your development environment is ready!

To run Kosmorro, invoke `poetry run kosmorro`. For comfort, you may also want to invoke `poetry shell`, which will expose the `kosmorro` command directly.

## Using Kosmorro

Using Kosmorro is as simple as invoking `kosmorro` in your terminal!

By default, it will give you the current Moon phase and, if any, the events that will occur today.

Kosmorro has a lot of available options to get exactly what you want, including the possibility to get planets rise and set. To get a list of them, run `kosmorro --help`, or read its manual with `man kosmorro`. You can also find usage examples in [the `tldr` manual](https://tldr.sh) with [`tldr kosmorro`](https://tldr.inbrowser.app/pages/common/kosmorro).

## Help translating Kosmorro!

Kosmorro is translated on [Weblate](https://hosted.weblate.org/engage/kosmorro/), a popular free platform for crowd-sourced internationalization.
If you speak a language that is not supported yet, feel free to contribute!

![Translation state per language](https://hosted.weblate.org/widgets/kosmorro/-/cli/multi-auto.svg)
