# ![Kosmorro](assets/png/kosmorro-logo.png)
![PyPI - Status](https://img.shields.io/pypi/status/kosmorro) ![PyPI](https://img.shields.io/pypi/v/kosmorro)

## About the project

Kosmorro is a software that allows you to compute the ephemeris for a date, a month or a year.

## Installation

### Requirements

Kosmorro requires the following software to work:

- Python ≥ 3.7.0
- PIP

Note: Kosmorro currently only supports Linux operating system. macOS will follow soon. Windows probably.

### Production environment

#### Linux

##### Arch Linux, Manjaro…

Kosmorro is available [in the AUR](https://aur.archlinux.org/packages/kosmorro).

##### Other distributions

Kosmorro is available [on PyPI](https://pypi.org/project/kosmorro/), a repository dedicated to Python.
First, install `python-pip` on your system and invoke the following command: `pip install kosmorro`.

#### Windows, macOS

Kosmorro being at an early-stage development, Windows and macOS are not supported officially for now.

### Development environment

First, install [Pipenv](https://pypi.org/project/pipenv/).

Clone this repository and run `pipenv sync` to install all the dependencies.
Then, run Kosmorro by invoking `pipenv run python kosmorro`.

For comfort, you may want to invoke `pipenv shell` first and then just `python kosmoro`.

## Running Kosmorro

### Usage

```
kosmorro [-h] [--latitude LATITUDE] [--longitude LONGITUDE]
         [--altitude ALTITUDE] [--day DAY] [--month MONTH]
         [--year YEAR]

Compute the ephemerides for a given date, at a given position on Earth.

optional arguments:
  -h, --help            show this help message and exit
  --latitude LATITUDE, -lat LATITUDE
                        The observer's latitude on Earth
  --longitude LONGITUDE, -lon LONGITUDE
                        The observer's longitude on Earth
  --altitude ALTITUDE, -alt ALTITUDE
                        The observer's altitude on Earth
  --day DAY, -d DAY     A number between 1 and 28, 29, 30 or 31 (depending on
                        the month). The day you want to compute the
                        ephemerides for. Defaults to 10 (the current day).
  --month MONTH, -m MONTH
                        A number between 1 and 12. The month you want to
                        compute the ephemerides for. Defaults to 11 (the
                        current month).
  --year YEAR, -y YEAR  The year you want to compute the ephemerides for.
                        Defaults to 2019 (the current year).

By default, the ephemerides will be computed for today (Sun Nov 10, 2019) for
an observer positioned at coordinates (0,0), with an altitude of 0.
```

For instance, if you want the ephemeris of October 31th, 2019 in Paris, France:

```console
$ python kosmorro.py --latitude 48.8032 --longitude 2.3511 -d 11 -m 11 -y 2019
Ephemerides of Sunday November 10, 2019

Planet     Rise time    Culmination time    Set time
--------  -----------  ------------------  ----------
Sun          06:52           11:34           06:52
Moon         16:12             -             05:17
Mercury      06:57           11:36           06:57
Venus        09:00           13:10           09:00
Mars         04:38           10:02           04:38
Jupiter      10:00           14:09           10:00
Saturn       11:25           15:38           11:25
Uranus       15:33           22:35           05:41
Neptune      14:03           19:38           01:16
Pluto        11:46           15:59           11:46

Moon phase: First Quarter

Note: All the hours are given in UTC.
```
