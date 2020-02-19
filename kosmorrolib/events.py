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
from skyfield.searchlib import find_discrete, find_maxima

from .data import Event, Planet, ASTERS
from .core import get_timescale, get_skf_objects, flatten_list


def _search_conjunction(start_time: Time, end_time: Time) -> [Event]:
    earth = get_skf_objects()['earth']
    aster1 = None
    aster2 = None

    def is_in_conjunction(time: Time):
        earth_pos = earth.at(time)
        aster1_pos = earth_pos.observe(get_skf_objects()[aster1.skyfield_name]).apparent()
        aster2_pos = earth_pos.observe(get_skf_objects()[aster2.skyfield_name]).apparent()

        aster_1_right_ascension, _, _ = aster1_pos.radec()
        aster_2_right_ascension, _, _ = aster2_pos.radec()

        return aster_1_right_ascension.hours - aster_2_right_ascension.hours < 0

    is_in_conjunction.rough_period = 1.0

    computed = []
    conjunctions = []

    for aster1 in ASTERS:
        # Ignore the Sun
        if not isinstance(aster1, Planet):
            continue

        for aster2 in ASTERS:
            if not isinstance(aster2, Planet) or aster2 == aster1 or aster2 in computed:
                continue

            times, _ = find_discrete(start_time, end_time, is_in_conjunction)

            for time in times:
                conjunctions.append(Event('CONJUNCTION', [aster1, aster2], time.utc_datetime()))

        computed.append(aster1)

    return conjunctions


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
            events.append(Event('OPPOSITION', [aster], time.utc_datetime()))

    return events


def _search_maximal_elongations(start_time: Time, end_time: Time) -> [Event]:
    earth = get_skf_objects()['earth']
    sun = get_skf_objects()['sun']
    aster = None

    def get_elongation(time: Time):
        sun_pos = (sun - earth).at(time)
        aster_pos = (aster.get_skyfield_object() - earth).at(time)
        separation = sun_pos.separation_from(aster_pos)
        return separation.degrees

    get_elongation.rough_period = 1.0

    events = []

    for aster in ASTERS:
        if aster.skyfield_name not in ['MERCURY', 'VENUS']:
            continue

        times, elongations = find_maxima(start_time, end_time, f=get_elongation, epsilon=1./24/3600, num=12)

        for i, time in enumerate(times):
            elongation = elongations[i]
            events.append(Event('MAXIMAL_ELONGATION', [aster], time.utc_datetime(),
                                details='{:.3n}°'.format(elongation)))

    return events


def search_events(date: date_type) -> [Event]:
    start_time = get_timescale().utc(date.year, date.month, date.day)
    end_time = get_timescale().utc(date.year, date.month, date.day + 1)

    return sorted(flatten_list([
        _search_oppositions(start_time, end_time),
        _search_conjunction(start_time, end_time),
        _search_maximal_elongations(start_time, end_time)
    ]), key=lambda event: event.start_time)
