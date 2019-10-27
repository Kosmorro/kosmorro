# ![Kosmorro](assets/png/kosmorro-logo.png)

## About the project

Kosmorro is a software that allows you to compute the ephemeris for a date, a month or a year.

## Installation

### Requirements

To use this software, you will need the following software:

- Python ≥ 3.7.0
- PIP
- [Pipenv](https://pypi.org/project/pipenv/)

Clone this repository and run `pipenv sync` to install all the dependencies.

# Running Kosmorro

Because it's still on an early-development stage, to run Kosmorro, you will need to prefix your commands `pipenv run`.
A `setup.py` file will come later to manage installation in the real world.

## Usage

```
kosmorro.py [-h] [--latitude LATITUDE] [--longitude LONGITUDE]
            [--altitude ALTITUDE] [--date DATE] [--month MONTH]
            year

Compute the ephemeris for a given day/month/year.

positional arguments:
  year                  The year you want to compute the ephemeris for

optional arguments:
  -h, --help            show this help message and exit
  --latitude LATITUDE, -lat LATITUDE
                        The observer's position on Earth (latitude)
  --longitude LONGITUDE, -lon LONGITUDE
                        The observer's position on Earth (longitude)
  --altitude ALTITUDE, -alt ALTITUDE
                        The observer's position on Earth (altitude)
  --date DATE, -d DATE  A number between 1 and 28, 29, 30 or 31 (depending on
                        the month). The date you want to compute the ephemeris
                        for
  --month MONTH, -m MONTH
                        A number between 1 and 12. The month you want to
                        compute the ephemeris for (defaults to the current
                        month if the day is defined)

By default, the observer will be set at position (0,0) with an altitude of 0.
You will more likely want to change that.
```

For instance, if you want the ephemeris of October 31th, 2019 in Paris, France:

```console
$ python kosmorro.py --latitude 48.8032 --longitude 2.3511 -m 10 -d 31 2019
Planet     Rise time    Maximum time    Set time
--------  -----------  --------------  ----------
SUN          06:35           -           16:32
MERCURY      08:44         13:01         16:59
VENUS        08:35         13:01         17:18
MARS         04:48         10:20         15:51
JUPITER      10:40         15:01         18:46
SATURN       12:12         16:20         20:26
URANUS       16:23           -           06:22
NEPTUNE      14:53         20:23         01:56
PLUTO        12:36         17:01         20:50

Moon phase: New Moon
```