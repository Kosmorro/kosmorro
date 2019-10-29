#    Kosmorro - Compute The Next Ephemeris
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

from multiprocessing import Pool as ThreadPool
from skyfield.api import Loader, Topos
from skyfield import almanac


class Ephemeris:
    MONTH = ['JAN', 'FEB', 'MAR', 'APR', 'MAY', 'JUN', 'JUL', 'AUG', 'SEP', 'OCT', 'NOV', 'DEC']
    PLANETS = ['MERCURY', 'VENUS', 'MARS', 'JUPITER BARYCENTER', 'SATURN BARYCENTER', 'URANUS BARYCENTER',
               'NEPTUNE BARYCENTER', 'PLUTO BARYCENTER']
    position = None
    latitude = None
    longitude = None
    timescale = None
    planets = None

    def __init__(self, position):
        load = Loader('./cache')
        self.timescale = load.timescale()
        self.planets = load('de421.bsp')
        self.latitude = position['lat']
        self.longitude = position['lon']
        self.position = Topos(latitude_degrees=position['lat'], longitude_degrees=position['lon'])

    def compute_ephemeris_for_day(self, year: int, month: int, day: int) -> dict:
        ephemeris = {}
        time1 = self.timescale.utc(year, month, day, 2)
        time2 = self.timescale.utc(year, month, day + 1, 2)

        # Compute sunrise and sunset
        ephemeris['sun'] = self.get_sun(time1, time2)
        ephemeris['moon'] = self.get_moon(year, month, day)
        ephemeris['planets'] = self.get_planets(year, month, day)

        return ephemeris

    def get_sun(self, time1, time2) -> dict:
        t, y = almanac.find_discrete(time1, time2, almanac.sunrise_sunset(self.planets, self.position))

        sunrise = t[0] if y[0] else t[1]
        sunset = t[1] if not y[1] else t[0]

        return {'rise': sunrise, 'set': sunset}

    def get_moon(self, year, month, day) -> dict:
        time1 = self.timescale.utc(year, month, day - 10)
        time2 = self.timescale.utc(year, month, day)

        _, y = almanac.find_discrete(time1, time2, almanac.moon_phases(self.planets))

        return {'phase': y[-1]}

    def get_planets(self, year: int, month: int, day: int) -> dict:
        args = []

        for planet_name in self.PLANETS:
            args.append({'planet': planet_name,
                         'observer': {'latitude': self.latitude, 'longitude': self.longitude},
                         'year': year, 'month': month, 'day': day})

        with ThreadPool(4) as pool:
            planets = pool.map(Ephemeris.get_planet, args)

        obj = {}

        for planet in planets:
            obj[planet['name'].split(' ')[0]] = {'rise': planet['rise'], 'maximum': planet['maximum'],
                                                 'set': planet['set']}

        return obj

    @staticmethod
    def get_planet(o) -> dict:
        load = Loader('./cache')
        planets = load('de421.bsp')
        timescale = load.timescale()
        position = Topos(latitude_degrees=o['observer']['latitude'], longitude_degrees=o['observer']['longitude'])
        observer = planets['earth'] + position
        planet = planets[o['planet']]
        rise_time = maximum_time = set_time = None
        max_elevation = None
        is_risen = None
        is_elevating = None
        last_is_elevating = None
        last_position = None

        for hours in range(0, 24):
            time = timescale.utc(o['year'], o['month'], o['day'], hours)
            position = observer.at(time).observe(planet).apparent().altaz()[0].degrees

            if is_risen is None:
                is_risen = position > 0
            if last_position is not None:
                is_elevating = last_position < position

            if rise_time is None and not is_risen and is_elevating and position > 0:
                # Planet has risen in the last hour, let's look for a more precise time!
                for minutes in range(0, 60):
                    time = timescale.utc(o['year'], o['month'], o['day'], hours - 1, minutes)
                    position = observer.at(time).observe(planet).apparent().altaz()[0].degrees

                    if position > 0:
                        # Planet has just risen!
                        rise_time = time
                        is_risen = True
                        break

            if set_time is None and is_risen and not is_elevating and position < 0:
                # Planet has set in the last hour, let's look for a more precise time!
                for minutes in range(0, 60):
                    time = timescale.utc(o['year'], o['month'], o['day'], hours - 1, minutes)
                    position = observer.at(time).observe(planet).apparent().altaz()[0].degrees

                    if position < 0:
                        # Planet has just set!
                        set_time = time
                        is_risen = False
                        break

            if not is_elevating and last_is_elevating:
                # Planet has reached its azimuth in the last hour, let's look for a more precise time!
                for minutes in range(0, 60):
                    time = timescale.utc(o['year'], o['month'], o['day'], hours - 1, minutes)
                    position = observer.at(time).observe(planet).apparent().altaz()[0].degrees

                    max_elevation = position
                    maximum_time = time

                    if last_position > position:
                        # Planet has reached its azimuth!
                        is_elevating = False
                        break

                    last_position = position

            last_position = position
            last_is_elevating = is_elevating

            if rise_time is not None and set_time is not None and maximum_time is not None:
                return {
                    'name': o['planet'],
                    'rise': rise_time,
                    'maximum': maximum_time,
                    'set': set_time
                }

        return {
            'name': o['planet'],
            'rise': rise_time if rise_time is not None else None,
            'maximum': maximum_time if maximum_time is not None else None,
            'set': set_time if set_time is not None else None
        }

    def compute_ephemeris_for_month(self, year: int, month: int) -> list:
        if month == 2:
            is_leap_year = (year % 4 == 0 and year % 100 > 0) or (year % 400 == 0)
            max_day = 29 if is_leap_year else 28
        elif month < 8:
            max_day = 30 if month % 2 == 0 else 31
        else:
            max_day = 31 if month % 2 == 0 else 30

        e = []

        for day in range(1, max_day + 1):
            e.append(self.compute_ephemeris_for_day(year, month, day))

        return e

    def compute_ephemeris_for_year(self, year: int) -> dict:
        e = {}
        for month in range(0, 12):
            e[self.MONTH[month]] = self.compute_ephemeris_for_month(year, month + 1)

        e['seasons'] = self.get_seasons(year)

        return e

    def get_seasons(self, year: int) -> dict:
        t1 = self.timescale.utc(year, 1, 1)
        t2 = self.timescale.utc(year, 12, 31)
        t, y = almanac.find_discrete(t1, t2, almanac.seasons(self.planets))

        seasons = {}
        for ti, yi in zip(t, y):
            if yi == 0:
                season = 'MARCH'
            elif yi == 1:
                season = 'JUNE'
            elif yi == 2:
                season = 'SEPTEMBER'
            elif yi == 3:
                season = 'DECEMBER'
            else:
                raise AssertionError

            seasons[season] = ti.utc_iso()

        return seasons

    def compute_ephemeris(self, year: int, month: int, day: int):
        if day is not None:
            return self.compute_ephemeris_for_day(year, month, day)
        elif month is not None:
            return self.compute_ephemeris_for_month(year, month)
        else:
            return self.compute_ephemeris_for_year(year)
