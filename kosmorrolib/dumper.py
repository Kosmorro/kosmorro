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

from abc import ABC, abstractmethod
import datetime
from tabulate import tabulate
from skyfield import almanac
from .data import Object


class Dumper(ABC):
    def __init__(self, ephemeris, date: datetime.date = datetime.date.today()):
        self.ephemeris = ephemeris
        self.date = date

    @abstractmethod
    def to_string(self):
        pass


class TextDumper(Dumper):
    def to_string(self):
        return '\n\n'.join(['Ephemerides of %s' % self.date.strftime('%A %B %d, %Y'),
                            self.get_asters(self.ephemeris['planets']),
                            self.get_moon(self.ephemeris['moon_phase']),
                            'Note: All the hours are given in UTC.'])

    @staticmethod
    def get_asters(asters: [Object]) -> str:
        data = []

        for aster in asters:
            name = aster.name

            if aster.ephemerides.rise_time is not None:
                planet_rise = aster.ephemerides.rise_time.utc_strftime('%H:%M')
            else:
                planet_rise = '-'

            if aster.ephemerides.maximum_time is not None:
                planet_maximum = aster.ephemerides.maximum_time.utc_strftime('%H:%M')
            else:
                planet_maximum = '-'

            if aster.ephemerides.set_time is not None:
                planet_set = aster.ephemerides.set_time.utc_strftime('%H:%M')
            else:
                planet_set = '-'

            data.append([name, planet_rise, planet_maximum, planet_set])

        return tabulate(data, headers=['Planet', 'Rise time', 'Culmination time', 'Set time'], tablefmt='simple',
                        stralign='center', colalign=('left',))

    @staticmethod
    def get_moon(moon):
        return 'Moon phase: %s' % almanac.MOON_PHASES[moon['phase']]
