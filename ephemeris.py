from skyfield.api import Loader, Topos
from skyfield import almanac


class Ephemeris:
    position = None
    timescale = None
    planets = None

    def __init__(self, position):
        self.MONTH = ['JAN', 'FEB', 'MAR', 'APR', 'MAY', 'JUN', 'JUL', 'AUG', 'SEP', 'OCT', 'NOV', 'DEC']
        self.PLANETS = ['mercury', 'venus', 'mars', 'jupiter', 'saturn', 'uranus', 'neptune', 'pluto']

        load = Loader('./cache')
        self.timescale = load.timescale()
        self.planets = load('de421.bsp')

        self.position = Topos(latitude_degrees=position['lat'], longitude_degrees=position['lon'])

    def compute_ephemeris_for_day(self, year: int, month: int, day: int) -> dict:
        ephemeris = {}
        time1 = self.timescale.utc(year, month, day, 2)
        time2 = self.timescale.utc(year, month, day + 1, 2)

        # Compute sunrise and sunset
        ephemeris['sun'] = self.get_sun(time1, time2)
        ephemeris['moon'] = self.get_moon(year, month, day)

        return ephemeris

    def get_sun(self, time1, time2) -> dict:
        t, y = almanac.find_discrete(time1, time2, almanac.sunrise_sunset(self.planets, self.position))

        sunrise = t[0] if y[0] else t[1]
        sunset = t[1] if not y[1] else t[0]

        return {'rise': sunrise.utc_iso(), 'set': sunset.utc_iso()}

    def get_moon(self, year, month, day) -> dict:
        time1 = self.timescale.utc(year, month, day - 10)
        time2 = self.timescale.utc(year, month, day)

        _, y = almanac.find_discrete(time1, time2, almanac.moon_phases(self.planets))

        return {'phase': y[-1]}

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
