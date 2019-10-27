from abc import ABC, abstractmethod
from tabulate import tabulate
from skyfield import almanac


class Dumper(ABC):
    def __init__(self, ephemeris):
        self.ephemeris = ephemeris

    @abstractmethod
    def to_string(self):
        pass


class TextDumper(Dumper):
    def to_string(self):
        s = '\n\n'.join([self.get_planets(self.ephemeris['planets'], self.ephemeris['sun']),
                         self.get_moon(self.ephemeris['moon'])])
        return s

    @staticmethod
    def get_planets(planets, sun):
        s = [['SUN', sun['rise'].utc_strftime('%H:%M'), '-', sun['set'].utc_strftime('%H:%M')]]
        for planet in planets:
            name = planet
            planet_data = planets[planet]
            planet_rise = planet_data['rise'].utc_strftime('%H:%M') if planet_data['rise'] is not None else '  -'
            planet_maximum = planet_data['maximum'].utc_strftime('%H:%M') if planet_data['maximum'] is not None\
                                                                          else '  -'
            planet_set = planet_data['set'].utc_strftime('%H:%M') if planet_data['set'] is not None else '  -'

            s.append([name, planet_rise, planet_maximum, planet_set])

        return tabulate(s, headers=['Planet', 'Rise time', 'Maximum time', 'Set time'], tablefmt='simple',
                        stralign='center', colalign=('left',))

    @staticmethod
    def get_moon(moon):
        return 'Moon phase: %s' % almanac.MOON_PHASES[moon['phase']]
