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
from skyfield import almanac
from skyfield.timelib import Time

from .data import Object, Position, AsterEphemerides, skyfield_to_moon_phase
from .core import get_skf_objects, get_timescale, ASTERS, MONTHS

RISEN_ANGLE = -0.8333


class EphemeridesComputer:
    def __init__(self, position: Position):
        position.observation_planet = get_skf_objects()['earth']
        self.position = position

    def get_sun(self, start_time, end_time) -> dict:
        times, is_risen = almanac.find_discrete(start_time,
                                                end_time,
                                                almanac.sunrise_sunset(get_skf_objects(), self.position))

        sunrise = times[0] if is_risen[0] else times[1]
        sunset = times[1] if not is_risen[1] else times[0]

        return {'rise': sunrise, 'set': sunset}

    @staticmethod
    def get_moon(year, month, day) -> str:
        time1 = get_timescale().utc(year, month, day - 10)
        time2 = get_timescale().utc(year, month, day)

        _, moon_phase = almanac.find_discrete(time1, time2, almanac.moon_phases(get_skf_objects()))

        return skyfield_to_moon_phase(moon_phase[-1])

    @staticmethod
    def get_asters_ephemerides_for_aster(aster, date: datetime.date, position: Position) -> Object:
        skyfield_aster = get_skf_objects()[aster.skyfield_name]

        def get_angle(time: Time) -> float:
            return position.get_planet_topos().at(time).observe(skyfield_aster).apparent().altaz()[0].degrees

        def is_risen(time: Time) -> bool:
            return get_angle(time) > RISEN_ANGLE

        get_angle.rough_period = 1.0
        is_risen.rough_period = 0.5

        start_time = get_timescale().utc(date.year, date.month, date.day)
        end_time = get_timescale().utc(date.year, date.month, date.day, 23, 59, 59)

        rise_times, arr = almanac.find_discrete(start_time, end_time, is_risen)
        try:
            culmination_time, _ = almanac._find_maxima(start_time, end_time, get_angle, epsilon=1./3600/24)
        except ValueError:
            culmination_time = None

        if len(rise_times) == 2:
            rise_time = rise_times[0 if arr[0] else 1]
            set_time = rise_times[0 if not arr[1] else 0]
        else:
            rise_time = rise_times[0] if arr[0] else None
            set_time = rise_times[0] if not arr[0] else None

        culmination_time = culmination_time[0] if culmination_time is not None else None

        aster.ephemerides = AsterEphemerides(rise_time, culmination_time, set_time)
        return aster

    @staticmethod
    def is_leap_year(year: int) -> bool:
        return (year % 4 == 0 and year % 100 > 0) or (year % 400 == 0)

    def compute_ephemerides_for_day(self, year: int, month: int, day: int) -> dict:
        return {'moon_phase': self.get_moon(year, month, day),
                'details': [self.get_asters_ephemerides_for_aster(aster, datetime.date(year, month, day), self.position)
                            for aster in ASTERS]}

    def compute_ephemerides_for_month(self, year: int, month: int) -> [dict]:
        if month == 2:
            max_day = 29 if self.is_leap_year(year) else 28
        elif month < 8:
            max_day = 30 if month % 2 == 0 else 31
        else:
            max_day = 31 if month % 2 == 0 else 30

        ephemerides = []

        for day in range(1, max_day + 1):
            ephemerides.append(self.compute_ephemerides_for_day(year, month, day))

        return ephemerides

    def compute_ephemerides_for_year(self, year: int) -> [dict]:
        ephemerides = {'seasons': self.get_seasons(year)}

        for month in range(0, 12):
            ephemerides[MONTHS[month]] = self.compute_ephemerides_for_month(year, month + 1)

        return ephemerides

    @staticmethod
    def get_seasons(year: int) -> dict:
        start_time = get_timescale().utc(year, 1, 1)
        end_time = get_timescale().utc(year, 12, 31)
        times, almanac_seasons = almanac.find_discrete(start_time, end_time, almanac.seasons(get_skf_objects()))

        seasons = {}
        for time, almanac_season in zip(times, almanac_seasons):
            if almanac_season == 0:
                season = 'MARCH'
            elif almanac_season == 1:
                season = 'JUNE'
            elif almanac_season == 2:
                season = 'SEPTEMBER'
            elif almanac_season == 3:
                season = 'DECEMBER'
            else:
                raise AssertionError

            seasons[season] = time.utc_iso()

        return seasons

    def compute_ephemerides(self, year: int, month: int, day: int):
        if day is not None:
            return self.compute_ephemerides_for_day(year, month, day)

        if month is not None:
            return self.compute_ephemerides_for_month(year, month)

        return self.compute_ephemerides_for_year(year)
