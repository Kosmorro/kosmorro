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
from typing import Union

from skyfield.api import Loader
from skyfield.timelib import Time
from skyfield.nutationlib import iau2000b

from .data import Star, Planet, Satellite, MOON_PHASES, MoonPhase

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


def get_iau2000b(time: Time):
    return iau2000b(time.tt)


def clear_cache():
    rmtree(CACHE_FOLDER)


def skyfield_to_moon_phase(times: [Time], vals: [int], now: Time) -> Union[MoonPhase, None]:
    tomorrow = get_timescale().utc(now.utc_datetime().year, now.utc_datetime().month, now.utc_datetime().day + 1)

    phases = list(MOON_PHASES.keys())
    current_phase = None
    current_phase_time = None
    next_phase_time = None
    i = 0

    if len(times) == 0:
        return None

    for i, time in enumerate(times):
        if now.utc_iso() <= time.utc_iso():
            if vals[i] in [0, 2, 4, 6]:
                if time.utc_datetime() < tomorrow.utc_datetime():
                    current_phase_time = time
                    current_phase = phases[vals[i]]
                else:
                    i -= 1
                    current_phase_time = None
                    current_phase = phases[vals[i]]
            else:
                current_phase = phases[vals[i]]

            break

    for j in range(i + 1, len(times)):
        if vals[j] in [0, 2, 4, 6]:
            next_phase_time = times[j]
            break

    return MoonPhase(current_phase, current_phase_time, next_phase_time)
