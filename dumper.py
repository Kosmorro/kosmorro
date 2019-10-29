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
        return '\n\n'.join([self.get_planets(self.ephemeris['planets'], self.ephemeris['sun']),
                            self.get_moon(self.ephemeris['moon'])])

    @staticmethod
    def get_planets(planets, sun):
        data = [['SUN', sun['rise'].utc_strftime('%H:%M'), '-', sun['set'].utc_strftime('%H:%M')]]
        for planet in planets:
            name = planet
            planet_data = planets[planet]
            planet_rise = planet_data['rise'].utc_strftime('%H:%M') if planet_data['rise'] is not None else '  -'
            planet_maximum = planet_data['maximum'].utc_strftime('%H:%M') if planet_data['maximum'] is not None\
                                                                          else '  -'
            planet_set = planet_data['set'].utc_strftime('%H:%M') if planet_data['set'] is not None else '  -'

            data.append([name, planet_rise, planet_maximum, planet_set])

        return tabulate(data, headers=['Planet', 'Rise time', 'Maximum time', 'Set time'], tablefmt='simple',
                        stralign='center', colalign=('left',))

    @staticmethod
    def get_moon(moon):
        return 'Moon phase: %s' % almanac.MOON_PHASES[moon['phase']]
