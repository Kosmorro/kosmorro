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

import datetime
from typing import Union

from skyfield.searchlib import find_discrete, find_maxima
from skyfield.timelib import Time
from skyfield.constants import tau
from skyfield.errors import EphemerisRangeError

from .data import Position, AsterEphemerides, MoonPhase, Object, ASTERS
from .dateutil import translate_to_timezone
from .core import get_skf_objects, get_timescale, get_iau2000b
from .enum import MoonPhaseType
from .exceptions import OutOfRangeDateError

RISEN_ANGLE = -0.8333


def _get_skyfield_to_moon_phase(times: [Time], vals: [int], now: Time) -> Union[MoonPhase, None]:
    tomorrow = get_timescale().utc(now.utc_datetime().year, now.utc_datetime().month, now.utc_datetime().day + 1)

    phases = list(MoonPhaseType)
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

    return MoonPhase(current_phase,
                     current_phase_time.utc_datetime() if current_phase_time is not None else None,
                     next_phase_time.utc_datetime() if next_phase_time is not None else None)


def get_moon_phase(compute_date: datetime.date, timezone: int = 0) -> MoonPhase:
    earth = get_skf_objects()['earth']
    moon = get_skf_objects()['moon']
    sun = get_skf_objects()['sun']

    def moon_phase_at(time: Time):
        time._nutation_angles = get_iau2000b(time)
        current_earth = earth.at(time)
        _, mlon, _ = current_earth.observe(moon).apparent().ecliptic_latlon('date')
        _, slon, _ = current_earth.observe(sun).apparent().ecliptic_latlon('date')
        return (((mlon.radians - slon.radians) // (tau / 8)) % 8).astype(int)

    moon_phase_at.rough_period = 7.0  # one lunar phase per week

    today = get_timescale().utc(compute_date.year, compute_date.month, compute_date.day)
    time1 = get_timescale().utc(compute_date.year, compute_date.month, compute_date.day - 10)
    time2 = get_timescale().utc(compute_date.year, compute_date.month, compute_date.day + 10)

    try:
        times, phase = find_discrete(time1, time2, moon_phase_at)
    except EphemerisRangeError as error:
        start = translate_to_timezone(error.start_time.utc_datetime(), timezone)
        end = translate_to_timezone(error.end_time.utc_datetime(), timezone)

        start = datetime.date(start.year, start.month, start.day) + datetime.timedelta(days=12)
        end = datetime.date(end.year, end.month, end.day) - datetime.timedelta(days=12)

        raise OutOfRangeDateError(start, end)

    return _get_skyfield_to_moon_phase(times, phase, today)


def get_ephemerides(date: datetime.date, position: Position, timezone: int = 0) -> [AsterEphemerides]:
    ephemerides = []

    def get_angle(for_aster: Object):
        def fun(time: Time) -> float:
            return position.get_planet_topos().at(time).observe(for_aster.get_skyfield_object()).apparent().altaz()[0]\
                   .degrees
        fun.rough_period = 1.0
        return fun

    def is_risen(for_aster: Object):
        def fun(time: Time) -> bool:
            return get_angle(for_aster)(time) > RISEN_ANGLE
        fun.rough_period = 0.5
        return fun

    start_time = get_timescale().utc(date.year, date.month, date.day, -timezone)
    end_time = get_timescale().utc(date.year, date.month, date.day, 23 - timezone, 59, 59)

    try:
        for aster in ASTERS:
            rise_times, arr = find_discrete(start_time, end_time, is_risen(aster))
            try:
                culmination_time, _ = find_maxima(start_time, end_time, f=get_angle(aster), epsilon=1./3600/24, num=12)
                culmination_time = culmination_time[0] if len(culmination_time) > 0 else None
            except ValueError:
                culmination_time = None

            if len(rise_times) == 2:
                rise_time = rise_times[0 if arr[0] else 1]
                set_time = rise_times[1 if not arr[1] else 0]
            else:
                rise_time = rise_times[0] if arr[0] else None
                set_time = rise_times[0] if not arr[0] else None

            # Convert the Time instances to Python datetime objects
            if rise_time is not None:
                rise_time = translate_to_timezone(rise_time.utc_datetime().replace(microsecond=0),
                                                  to_tz=timezone)

            if culmination_time is not None:
                culmination_time = translate_to_timezone(culmination_time.utc_datetime().replace(microsecond=0),
                                                         to_tz=timezone)

            if set_time is not None:
                set_time = translate_to_timezone(set_time.utc_datetime().replace(microsecond=0),
                                                 to_tz=timezone)

            ephemerides.append(AsterEphemerides(rise_time, culmination_time, set_time, aster=aster))
    except EphemerisRangeError as error:
        start = translate_to_timezone(error.start_time.utc_datetime(), timezone)
        end = translate_to_timezone(error.end_time.utc_datetime(), timezone)

        start = datetime.date(start.year, start.month, start.day + 1)
        end = datetime.date(end.year, end.month, end.day - 1)

        raise OutOfRangeDateError(start, end)

    return ephemerides
