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
from datetime import datetime

from numpy import pi, arcsin

from skyfield.api import Topos, Time
from skyfield.vectorlib import VectorSum as SkfPlanet

from .core import get_skf_objects
from .enum import MoonPhaseType, EventType
from .i18n import _


class Serializable(ABC):
    @abstractmethod
    def serialize(self) -> dict:
        pass


class MoonPhase(Serializable):
    def __init__(self, phase_type: MoonPhaseType, time: datetime = None, next_phase_date: datetime = None):
        self.phase_type = phase_type
        self.time = time
        self.next_phase_date = next_phase_date

    def get_next_phase(self):
        if self.phase_type in [MoonPhaseType.NEW_MOON, MoonPhaseType.WAXING_CRESCENT]:
            return MoonPhaseType.FIRST_QUARTER
        if self.phase_type in [MoonPhaseType.FIRST_QUARTER, MoonPhaseType.WAXING_GIBBOUS]:
            return MoonPhaseType.FULL_MOON
        if self.phase_type in [MoonPhaseType.FULL_MOON, MoonPhaseType.WANING_GIBBOUS]:
            return MoonPhaseType.LAST_QUARTER

        return MoonPhaseType.NEW_MOON

    def serialize(self) -> dict:
        return {
            'phase': self.phase_type.name,
            'time': self.time.isoformat() if self.time is not None else None,
            'next': {
                'phase': self.get_next_phase().name,
                'time': self.next_phase_date.isoformat()
            }
        }


class Object(Serializable):
    """
    An astronomical object.
    """

    def __init__(self,
                 name: str,
                 skyfield_name: str,
                 radius: float = None):
        """
        Initialize an astronomical object

        :param str name: the official name of the object (may be internationalized)
        :param str skyfield_name: the internal name of the object in Skyfield library
        :param float radius: the radius (in km) of the object
        :param AsterEphemerides ephemerides: the ephemerides associated to the object
        """
        self.name = name
        self.skyfield_name = skyfield_name
        self.radius = radius

    def __repr__(self):
        return '<Object type=%s name=%s />' % (self.get_type(), self.name)

    def get_skyfield_object(self) -> SkfPlanet:
        return get_skf_objects()[self.skyfield_name]

    @abstractmethod
    def get_type(self) -> str:
        pass

    def get_apparent_radius(self, time: Time, from_place) -> float:
        """
        Calculate the apparent radius, in degrees, of the object from the given place at a given time.
        :param time:
        :param from_place:
        :return:
        """
        if self.radius is None:
            raise ValueError('Missing radius for %s object' % self.name)

        return 360 / pi * arcsin(self.radius / from_place.at(time).observe(self.get_skyfield_object()).distance().km)

    def serialize(self) -> dict:
        return {
            'name': self.name,
            'type': self.get_type(),
            'radius': self.radius,
        }


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


class Event(Serializable):
    def __init__(self, event_type: EventType, objects: [Object], start_time: datetime,
                 end_time: Union[datetime, None] = None, details: str = None):
        self.event_type = event_type
        self.objects = objects
        self.start_time = start_time
        self.end_time = end_time
        self.details = details

    def __repr__(self):
        return '<Event type=%s objects=[%s] start=%s end=%s details=%s>' % (self.event_type,
                                                                            self.objects,
                                                                            self.start_time,
                                                                            self.end_time,
                                                                            self.details)

    def get_description(self, show_details: bool = True) -> str:
        description = self.event_type.value % self._get_objects_name()
        if show_details and self.details is not None:
            description += ' ({:s})'.format(self.details)
        return description

    def _get_objects_name(self):
        if len(self.objects) == 1:
            return self.objects[0].name

        return tuple(object.name for object in self.objects)

    def serialize(self) -> dict:
        return {
            'objects': [object.serialize() for object in self.objects],
            'event': self.event_type.name,
            'starts_at': self.start_time.isoformat(),
            'ends_at': self.end_time.isoformat() if self.end_time is not None else None,
            'details': self.details
        }


class AsterEphemerides(Serializable):
    def __init__(self,
                 rise_time: Union[datetime, None],
                 culmination_time: Union[datetime, None],
                 set_time: Union[datetime, None],
                 aster: Object):
        self.rise_time = rise_time
        self.culmination_time = culmination_time
        self.set_time = set_time
        self.object = aster

    def serialize(self) -> dict:
        return {
            'object': self.object.serialize(),
            'rise_time': self.rise_time.isoformat() if self.rise_time is not None else None,
            'culmination_time': self.culmination_time.isoformat() if self.culmination_time is not None else None,
            'set_time': self.set_time.isoformat() if self.set_time is not None else None
        }


EARTH = Planet('Earth', 'EARTH')

ASTERS = [Star(_('Sun'), 'SUN', radius=696342),
          Satellite(_('Moon'), 'MOON', radius=1737.4),
          Planet(_('Mercury'), 'MERCURY', radius=2439.7),
          Planet(_('Venus'), 'VENUS', radius=6051.8),
          Planet(_('Mars'), 'MARS', radius=3396.2),
          Planet(_('Jupiter'), 'JUPITER BARYCENTER', radius=71492),
          Planet(_('Saturn'), 'SATURN BARYCENTER', radius=60268),
          Planet(_('Uranus'), 'URANUS BARYCENTER', radius=25559),
          Planet(_('Neptune'), 'NEPTUNE BARYCENTER', radius=24764),
          Planet(_('Pluto'), 'PLUTO BARYCENTER', radius=1185)]


class Position:
    def __init__(self, latitude: float, longitude: float, aster: Object):
        self.latitude = latitude
        self.longitude = longitude
        self.aster = aster
        self._topos = None

    def get_planet_topos(self) -> Topos:
        if self.aster is None:
            raise TypeError('Observation planet must be set.')

        if self._topos is None:
            self._topos = self.aster.get_skyfield_object() + Topos(latitude_degrees=self.latitude,
                                                                   longitude_degrees=self.longitude)

        return self._topos
