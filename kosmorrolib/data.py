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
from typing import Union

from skyfield.api import Topos
from skyfield.timelib import Time

MOON_PHASES = {
    'NEW_MOON': 'New Moon',
    'WAXING_CRESCENT': 'Waxing crescent',
    'FIRST_QUARTER': 'First Quarter',
    'WAXING_GIBBOUS': 'Waxing gibbous',
    'FULL_MOON': 'Full Moon',
    'WANING_GIBBOUS': 'Waning gibbous',
    'LAST_QUARTER': 'Last Quarter',
    'WANING_CRESCENT': 'Waning crescent'
}


class MoonPhase:
    def __init__(self, identifier: str, time: Union[Time, None], next_phase_date: Union[Time, None]):
        if identifier not in MOON_PHASES.keys():
            raise ValueError('identifier parameter must be one of %s (got %s)' % (', '.join(MOON_PHASES.keys()),
                                                                                  identifier))

        self.identifier = identifier
        self.time = time
        self.next_phase_date = next_phase_date

    def get_phase(self):
        return MOON_PHASES[self.identifier]

    def get_next_phase(self):
        if self.identifier == 'NEW_MOON':
            next_identifier = 'FIRST_QUARTER'
        elif self.identifier == 'FIRST_QUARTER':
            next_identifier = 'FULL_MOON'
        elif self.identifier == 'FULL_MOON':
            next_identifier = 'LAST_QUARTER'
        else:
            next_identifier = 'NEW_MOON'

        return MOON_PHASES[next_identifier]


class Position:
    def __init__(self, latitude: float, longitude: float):
        self.latitude = latitude
        self.longitude = longitude
        self.observation_planet = None
        self._topos = None

    def get_planet_topos(self) -> Topos:
        if self.observation_planet is None:
            raise TypeError('Observation planet must be set.')

        if self._topos is None:
            self._topos = self.observation_planet + Topos(latitude_degrees=self.latitude,
                                                          longitude_degrees=self.longitude)

        return self._topos


class AsterEphemerides:
    def __init__(self,
                 rise_time: Union[Time, None],
                 culmination_time: Union[Time, None],
                 set_time: Union[Time, None]):
        self.rise_time = rise_time
        self.culmination_time = culmination_time
        self.set_time = set_time


class Object(ABC):
    """
    An astronomical object.
    """

    def __init__(self,
                 name: str,
                 skyfield_name: str,
                 ephemerides: AsterEphemerides or None = None):
        """
        Initialize an astronomical object

        :param str name: the official name of the object (may be internationalized)
        :param str skyfield_name: the internal name of the object in Skyfield library
        :param AsterEphemerides ephemerides: the ephemerides associated to the object
        """
        self.name = name
        self.skyfield_name = skyfield_name
        self.ephemerides = ephemerides

    @abstractmethod
    def get_type(self) -> str:
        pass


class Star(Object):
    def get_type(self) -> str:
        return 'star'


class Planet(Object):
    def get_type(self) -> str:
        return 'planet'


class DwarfPlanet(Planet):
    def get_type(self) -> str:
        return 'dwarf_planet'


class Satellite(Object):
    def get_type(self) -> str:
        return 'satellite'
