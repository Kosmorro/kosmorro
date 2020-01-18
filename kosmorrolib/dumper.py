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
from termcolor import colored
from .data import Object, AsterEphemerides, MoonPhase, Event
from .i18n import _

FULL_DATE_FORMAT = _('{day_of_week} {month} {day_number}, {year}').format(day_of_week='%A', month='%B',
                                                                          day_number='%d', year='%Y')
TIME_FORMAT = _('{hours}:{minutes}').format(hours='%H', minutes='%M')


class Dumper(ABC):
    def __init__(self, ephemeris: dict, events: [Event], date: datetime.date = datetime.date.today(),
                 with_colors: bool = True):
        self.ephemeris = ephemeris
        self.events = events
        self.date = date
        self.with_colors = with_colors

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
            event['objects'] = [object.name for object in event['objects']]
            return event

        raise TypeError('Object of type "%s" could not be integrated in the JSON' % str(type(obj)))


class TextDumper(Dumper):
    def to_string(self):
        text = [self.style(self.get_date(), 'h1')]

        if len(self.ephemeris['details']) > 0:
            text.append(self.get_asters(self.ephemeris['details']))

        text.append(self.get_moon(self.ephemeris['moon_phase']))

        if len(self.events) > 0:
            text.append('\n'.join([self.style(_('Expected events:'), 'h2'),
                                   self.get_events(self.events)]))

        text.append(self.style(_('Note: All the hours are given in UTC.'), 'em'))

        return '\n\n'.join(text)

    def style(self, text: str, tag: str) -> str:
        if not self.with_colors:
            return text

        styles = {
            'h1': lambda t: colored(t, 'yellow', attrs=['bold']),
            'h2': lambda t: colored(t, 'magenta', attrs=['bold']),
            'th': lambda t: colored(t, 'white', attrs=['bold']),
            'strong': lambda t: colored(t, attrs=['bold']),
            'em': lambda t: colored(t, attrs=['dark'])
        }

        return styles[tag](text)

    def get_date(self) -> str:
        date = self.date.strftime(FULL_DATE_FORMAT)

        return ''.join([date[0].upper(), date[1:]])

    def get_asters(self, asters: [Object]) -> str:
        data = []

        for aster in asters:
            name = self.style(aster.name, 'th')

            if aster.ephemerides.rise_time is not None:
                planet_rise = aster.ephemerides.rise_time.utc_strftime(TIME_FORMAT)
            else:
                planet_rise = '-'

            if aster.ephemerides.culmination_time is not None:
                planet_culmination = aster.ephemerides.culmination_time.utc_strftime(TIME_FORMAT)
            else:
                planet_culmination = '-'

            if aster.ephemerides.set_time is not None:
                planet_set = aster.ephemerides.set_time.utc_strftime(TIME_FORMAT)
            else:
                planet_set = '-'

            data.append([name, planet_rise, planet_culmination, planet_set])

        return tabulate(data, headers=[self.style(_('Object'), 'th'),
                                       self.style(_('Rise time'), 'th'),
                                       self.style(_('Culmination time'), 'th'),
                                       self.style(_('Set time'), 'th')],
                        tablefmt='simple', stralign='center', colalign=('left',))

    def get_events(self, events: [Event]) -> str:
        data = []

        for event in events:
            data.append([self.style(event.start_time.utc_strftime(TIME_FORMAT), 'th'),
                         event.get_description()])

        return tabulate(data, tablefmt='plain', stralign='left')

    def get_moon(self, moon_phase: MoonPhase) -> str:
        current_moon_phase = ' '.join([self.style(_('Moon phase:'), 'strong'), moon_phase.get_phase()])
        new_moon_phase = _('{next_moon_phase} on {next_moon_phase_date} at {next_moon_phase_time}').format(
            next_moon_phase=moon_phase.get_next_phase(),
            next_moon_phase_date=moon_phase.next_phase_date.utc_strftime(FULL_DATE_FORMAT),
            next_moon_phase_time=moon_phase.next_phase_date.utc_strftime(TIME_FORMAT)
        )

        return '\n'.join([current_moon_phase, new_moon_phase])
