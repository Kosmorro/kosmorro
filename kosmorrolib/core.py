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

from shutil import rmtree
from pathlib import Path
from skyfield.api import Loader

from .data import Star, Planet, Satellite

VERSION = '0.2.0'
CACHE_FOLDER = str(Path.home()) + '/.kosmorro-cache'

MONTHS = ['JAN', 'FEB', 'MAR', 'APR', 'MAY', 'JUN', 'JUL', 'AUG', 'SEP', 'OCT', 'NOV', 'DEC']

ASTERS = [Star('Sun', 'SUN'),
          Satellite('Moon', 'MOON'),
          Planet('Mercury', 'MERCURY'),
          Planet('Venus', 'VENUS'),
          Planet('Mars', 'MARS'),
          Planet('Jupiter', 'JUPITER BARYCENTER'),
          Planet('Saturn', 'SATURN BARYCENTER'),
          Planet('Uranus', 'URANUS BARYCENTER'),
          Planet('Neptune', 'NEPTUNE BARYCENTER'),
          Planet('Pluto', 'PLUTO BARYCENTER')]


def get_loader():
    return Loader(CACHE_FOLDER)


def get_timescale():
    return get_loader().timescale()


def get_skf_objects():
    return get_loader()('de421.bsp')


def clear_cache():
    rmtree(CACHE_FOLDER)
