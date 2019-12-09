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
import json
from tabulate import tabulate
from skyfield.timelib import Time
from numpy import int64
from .data import Object, AsterEphemerides, MoonPhase, Event


class Dumper(ABC):
    def __init__(self, ephemeris: dict, events: [Event], date: datetime.date = datetime.date.today()):
        self.ephemeris = ephemeris
        self.events = events
        self.date = date

    @abstractmethod
    def to_string(self):
        pass


class JsonDumper(Dumper):
    def to_string(self):
        self.ephemeris['events'] = self.events
        self.ephemeris['ephemerides'] = self.ephemeris.pop('details')
        return json.dumps(self.ephemeris,
                          default=self._json_default,
                          indent=4)

    @staticmethod
    def _json_default(obj):
        # Fixes the "TypeError: Object of type int64 is not JSON serializable"
        # See https://stackoverflow.com/a/50577730
        if isinstance(obj, int64):
            return int(obj)
        if isinstance(obj, Time):
            return obj.utc_iso()
        if isinstance(obj, Object):
            obj = obj.__dict__
            obj.pop('skyfield_name')
            obj['object'] = obj.pop('name')
            obj['details'] = obj.pop('ephemerides')
            return obj
        if isinstance(obj, AsterEphemerides):
            return obj.__dict__
        if isinstance(obj, MoonPhase):
            moon_phase = obj.__dict__
            moon_phase['phase'] = moon_phase.pop('identifier')
            moon_phase['date'] = moon_phase.pop('time')
            return moon_phase
        if isinstance(obj, Event):
            event = obj.__dict__
            event['object'] = event['object'].name
            return event

        raise TypeError('Object of type "%s" could not be integrated in the JSON' % str(type(obj)))


class TextDumper(Dumper):
    def to_string(self):
        text = self.date.strftime('%A %B %d, %Y')

        if len(self.ephemeris['details']) > 0:
            text = '\n\n'.join([text,
                                self.get_asters(self.ephemeris['details'])
                                ])

        text = '\n\n'.join([text,
                            self.get_moon(self.ephemeris['moon_phase'])
                            ])

        if len(self.events) > 0:
            text = '\n\n'.join([text,
                                'Expected events:',
                                self.get_events(self.events)
                                ])

        text = '\n\n'.join([text, 'Note: All the hours are given in UTC.'])

        return text

    @staticmethod
    def get_asters(asters: [Object]) -> str:
        data = []

        for aster in asters:
            name = aster.name

            if aster.ephemerides.rise_time is not None:
                planet_rise = aster.ephemerides.rise_time.utc_strftime('%H:%M')
            else:
                planet_rise = '-'

            if aster.ephemerides.culmination_time is not None:
                planet_culmination = aster.ephemerides.culmination_time.utc_strftime('%H:%M')
            else:
                planet_culmination = '-'

            if aster.ephemerides.set_time is not None:
                planet_set = aster.ephemerides.set_time.utc_strftime('%H:%M')
            else:
                planet_set = '-'

            data.append([name, planet_rise, planet_culmination, planet_set])

        return tabulate(data, headers=['Object', 'Rise time', 'Culmination time', 'Set time'], tablefmt='simple',
                        stralign='center', colalign=('left',))

    @staticmethod
    def get_events(events: [Event]) -> str:
        data = []

        for event in events:
            data.append([event.start_time.utc_strftime('%H:%M'), event.get_description()])

        return tabulate(data, tablefmt='plain', stralign='left')

    @staticmethod
    def get_moon(moon_phase: MoonPhase) -> str:
        return 'Moon phase: %s\n' \
               '%s on %s' % (moon_phase.get_phase(),
                             moon_phase.get_next_phase(),
                             moon_phase.next_phase_date.utc_strftime('%a %b %-d, %Y %H:%M'))
