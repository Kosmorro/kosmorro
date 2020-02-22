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
from skyfield.timelib import Time
from skyfield.nutationlib import iau2000b

CACHE_FOLDER = str(Path.home()) + '/.kosmorro-cache'


def get_loader():
    return Loader(CACHE_FOLDER)


def get_timescale():
    return get_loader().timescale()


def get_skf_objects():
    return get_loader()('de421.bsp')


def get_iau2000b(time: Time):
    return iau2000b(time.tt)


def clear_cache():
    rmtree(CACHE_FOLDER)


def flatten_list(the_list: list):
    new_list = []
    for item in the_list:
        if isinstance(item, list):
            for item2 in flatten_list(item):
                new_list.append(item2)
            continue

        new_list.append(item)

    return new_list
