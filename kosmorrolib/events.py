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

from datetime import date as date_type

from skyfield.timelib import Time
from skyfield.almanac import find_discrete

from .data import Event, Planet
from .core import get_timescale, get_skf_objects, ASTERS


def _search_oppositions(start_time: Time, end_time: Time) -> [Event]:
    earth = get_skf_objects()['earth']
    sun = get_skf_objects()['sun']
    aster = None

    def is_oppositing(time: Time) -> [bool]:
        earth_pos = earth.at(time)
        sun_pos = earth_pos.observe(sun).apparent()  # Never do this without eyes protection!
        aster_pos = earth_pos.observe(get_skf_objects()[aster.skyfield_name]).apparent()
        _, lon1, _ = sun_pos.ecliptic_latlon()
        _, lon2, _ = aster_pos.ecliptic_latlon()
        return (lon1.degrees - lon2.degrees) > 180

    is_oppositing.rough_period = 1.0
    events = []

    for aster in ASTERS:
        if not isinstance(aster, Planet) or aster.name in ['Mercury', 'Venus']:
            continue

        times, _ = find_discrete(start_time, end_time, is_oppositing)
        for time in times:
            events.append(Event('OPPOSITION', aster, time))

    return events


def search_events(date: date_type) -> [Event]:
    start_time = get_timescale().utc(date.year, date.month, date.day)
    end_time = get_timescale().utc(date.year, date.month, date.day + 1)

    return [
        opposition for opposition in _search_oppositions(start_time, end_time)
    ]
