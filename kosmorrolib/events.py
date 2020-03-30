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
from numpy import pi

from .data import Event, Star, Planet, ASTERS
from .core import get_timescale, get_skf_objects, flatten_list


def _search_conjunction(start_time: Time, end_time: Time) -> [Event]:
    earth = get_skf_objects()['earth']
    aster1 = None
    aster2 = None

    def is_in_conjunction(time: Time):
        earth_pos = earth.at(time)
        _, aster1_lon, _ = earth_pos.observe(aster1.get_skyfield_object()).apparent().ecliptic_latlon()
        _, aster2_lon, _ = earth_pos.observe(aster2.get_skyfield_object()).apparent().ecliptic_latlon()

        return ((aster1_lon.radians - aster2_lon.radians) / pi % 2.0).astype('int8') == 0

    is_in_conjunction.rough_period = 60.0

    computed = []
    conjunctions = []

    for aster1 in ASTERS:
        # Ignore the Sun
        if isinstance(aster1, Star):
            continue

        for aster2 in ASTERS:
            if isinstance(aster2, Star) or aster2 == aster1 or aster2 in computed:
                continue

            times, is_conjs = find_discrete(start_time, end_time, is_in_conjunction)

            for i, time in enumerate(times):
                if is_conjs[i]:
                    aster1_pos = (aster1.get_skyfield_object() - earth).at(time)
                    aster2_pos = (aster2.get_skyfield_object() - earth).at(time)
                    distance = aster1_pos.separation_from(aster2_pos).degrees

                    if distance - aster2.get_apparent_radius(time, earth) < aster1.get_apparent_radius(time, earth):
                        occulting_aster = [aster1,
                                           aster2] if aster1_pos.distance().km < aster2_pos.distance().km else [aster2,
                                                                                                                aster1]

                        conjunctions.append(Event('OCCULTATION', occulting_aster, time.utc_datetime()))
                    else:
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
        if not isinstance(aster, Planet) or aster.skyfield_name in ['MERCURY', 'VENUS']:
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
