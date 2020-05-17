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
import os
from pathlib import Path
from tabulate import tabulate
from numpy import int64
from termcolor import colored
from .data import ASTERS, Object, AsterEphemerides, MoonPhase, Event
from .i18n import _
from .version import VERSION
from .exceptions import UnavailableFeatureError
try:
    from latex import build_pdf
except ImportError:
    build_pdf = None

FULL_DATE_FORMAT = _('{day_of_week} {month} {day_number}, {year}').format(day_of_week='%A', month='%B',
                                                                          day_number='%d', year='%Y')
SHORT_DATETIME_FORMAT = _('{month} {day_number}, {hours}:{minutes}').format(month='%b', day_number='%d',
                                                                            hours='%H', minutes='%M')
TIME_FORMAT = _('{hours}:{minutes}').format(hours='%H', minutes='%M')


class Dumper(ABC):
    def __init__(self, ephemerides: [AsterEphemerides] = None, moon_phase: MoonPhase = None, events: [Event] = None,
                 date: datetime.date = datetime.date.today(), timezone: int = 0, with_colors: bool = True,
                 show_graph: bool = False):
        self.ephemerides = ephemerides
        self.moon_phase = moon_phase
        self.events = events
        self.date = date
        self.timezone = timezone
        self.with_colors = with_colors
        self.show_graph = show_graph

        if self.timezone != 0:
            self._convert_dates_to_timezones()

    def _convert_dates_to_timezones(self):
        if self.moon_phase.time is not None:
            self.moon_phase.time = self._datetime_to_timezone(self.moon_phase.time)
        if self.moon_phase.next_phase_date is not None:
            self.moon_phase.next_phase_date = self._datetime_to_timezone(
                self.moon_phase.next_phase_date)

        if self.ephemerides is not None:
            for ephemeris in self.ephemerides:
                if ephemeris.rise_time is not None:
                    ephemeris.rise_time = self._datetime_to_timezone(ephemeris.rise_time)
                if ephemeris.culmination_time is not None:
                    ephemeris.culmination_time = self._datetime_to_timezone(ephemeris.culmination_time)
                if ephemeris.set_time is not None:
                    ephemeris.set_time = self._datetime_to_timezone(ephemeris.set_time)

        for event in self.events:
            event.start_time = self._datetime_to_timezone(event.start_time)
            if event.end_time is not None:
                event.end_time = self._datetime_to_timezone(event.end_time)

    def _datetime_to_timezone(self, time: datetime.datetime):
        return time.replace(tzinfo=datetime.timezone.utc).astimezone(
            tz=datetime.timezone(
                datetime.timedelta(
                    hours=self.timezone
                )
            )
        )

    def get_date_as_string(self, capitalized: bool = False) -> str:
        date = self.date.strftime(FULL_DATE_FORMAT)

        if capitalized:
            return ''.join([date[0].upper(), date[1:]])

        return date

    @abstractmethod
    def to_string(self):
        pass

    @staticmethod
    def is_file_output_needed() -> bool:
        return False


class JsonDumper(Dumper):
    def to_string(self):
        return json.dumps({
            'ephemerides': [ephemeris.serialize() for ephemeris in self.ephemerides],
            'moon_phase': self.moon_phase.serialize(),
            'events': [event.serialize() for event in self.events]
        }, indent=4)

    @staticmethod
    def _json_default(obj):
        # Fixes the "TypeError: Object of type int64 is not JSON serializable"
        # See https://stackoverflow.com/a/50577730
        if isinstance(obj, int64):
            return int(obj)
        if isinstance(obj, datetime.datetime):
            return obj.isoformat()
        if isinstance(obj, Object):
            obj = obj.__dict__
            obj.pop('skyfield_name')
            obj.pop('radius')
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
        text = [self.style(self.get_date_as_string(capitalized=True), 'h1')]

        if self.ephemerides is not None:
            text.append(self.stringify_ephemerides())

        text.append(self.get_moon(self.moon_phase))

        if len(self.events) > 0:
            text.append('\n'.join([self.style(_('Expected events:'), 'h2'),
                                   self.get_events(self.events)]))

        if self.timezone == 0:
            text.append(self.style(_('Note: All the hours are given in UTC.'), 'em'))
        else:
            tz_offset = str(self.timezone)
            if self.timezone > 0:
                tz_offset = ''.join(['+', tz_offset])
            text.append(self.style(_('Note: All the hours are given in the UTC{offset} timezone.').format(
                offset=tz_offset), 'em'))

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

    def stringify_ephemerides(self) -> str:
        data = []

        for ephemeris in self.ephemerides:
            name = self.style(ephemeris.object.name, 'th')

            if ephemeris.rise_time is not None:
                time_fmt = TIME_FORMAT if ephemeris.rise_time.day == self.date.day else SHORT_DATETIME_FORMAT
                planet_rise = ephemeris.rise_time.strftime(time_fmt)
            else:
                planet_rise = '-'

            if ephemeris.culmination_time is not None:
                time_fmt = TIME_FORMAT if ephemeris.culmination_time.day == self.date.day \
                    else SHORT_DATETIME_FORMAT
                planet_culmination = ephemeris.culmination_time.strftime(time_fmt)
            else:
                planet_culmination = '-'

            if ephemeris.set_time is not None:
                time_fmt = TIME_FORMAT if ephemeris.set_time.day == self.date.day else SHORT_DATETIME_FORMAT
                planet_set = ephemeris.set_time.strftime(time_fmt)
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
            time_fmt = TIME_FORMAT if event.start_time.day == self.date.day else SHORT_DATETIME_FORMAT
            data.append([self.style(event.start_time.strftime(time_fmt), 'th'),
                         event.get_description()])

        return tabulate(data, tablefmt='plain', stralign='left')

    def get_moon(self, moon_phase: MoonPhase) -> str:
        current_moon_phase = ' '.join([self.style(_('Moon phase:'), 'strong'), moon_phase.get_phase()])
        new_moon_phase = _('{next_moon_phase} on {next_moon_phase_date} at {next_moon_phase_time}').format(
            next_moon_phase=moon_phase.get_next_phase_name(),
            next_moon_phase_date=moon_phase.next_phase_date.strftime(FULL_DATE_FORMAT),
            next_moon_phase_time=moon_phase.next_phase_date.strftime(TIME_FORMAT)
        )

        return '\n'.join([current_moon_phase, new_moon_phase])


class _LatexDumper(Dumper):
    def to_string(self):
        template_path = os.path.join(os.path.abspath(os.path.dirname(__file__)),
                                     'assets', 'pdf', 'template.tex')

        with open(template_path, mode='r') as file:
            template = file.read()

        return self._make_document(template)

    def _make_document(self, template: str) -> str:
        kosmorro_logo_path = os.path.join(os.path.abspath(os.path.dirname(__file__)),
                                          'assets', 'png', 'kosmorro-logo.png')
        moon_phase_graphics = os.path.join(os.path.abspath(os.path.dirname(__file__)),
                                           'assets', 'moonphases', 'png',
                                           '.'.join([self.moon_phase.identifier.lower().replace('_', '-'),
                                                     'png']))

        document = template

        if self.ephemerides is None:
            document = self._remove_section(document, 'ephemerides')

        if len(self.events) == 0:
            document = self._remove_section(document, 'events')

        document = self.add_strings(document, kosmorro_logo_path, moon_phase_graphics)

        if self.show_graph:
            # The graphephemerides environment beginning tag must end with a percent symbol to ensure
            # that no extra space will interfere with the graph.
            document = document.replace(r'\begin{ephemerides}', r'\begin{graphephemerides}%')\
                .replace(r'\end{ephemerides}', r'\end{graphephemerides}')

        return document

    def add_strings(self, document, kosmorro_logo_path, moon_phase_graphics) -> str:
        document = document \
            .replace('+++KOSMORRO-VERSION+++', VERSION) \
            .replace('+++KOSMORRO-LOGO+++', kosmorro_logo_path) \
            .replace('+++DOCUMENT-TITLE+++', _('A Summary of your Sky')) \
            .replace('+++DOCUMENT-DATE+++', self.get_date_as_string(capitalized=True)) \
            .replace('+++INTRODUCTION+++',
                     '\n\n'.join([
                         _("This document summarizes the ephemerides and the events of {date}. "
                           "It aims to help you to prepare your observation session. "
                           "All the hours are given in {timezone}.").format(
                               date=self.get_date_as_string(),
                               timezone='UTC+%d' % self.timezone if self.timezone != 0 else 'UTC'
                           ),
                         _("Don't forget to check the weather forecast before you go out with your equipment.")
                     ])) \
            .replace('+++SECTION-EPHEMERIDES+++', _('Ephemerides of the day')) \
            .replace('+++EPHEMERIDES-OBJECT+++', _('Object')) \
            .replace('+++EPHEMERIDES-RISE-TIME+++', _('Rise time')) \
            .replace('+++EPHEMERIDES-CULMINATION-TIME+++', _('Culmination time')) \
            .replace('+++EPHEMERIDES-SET-TIME+++', _('Set time')) \
            .replace('+++EPHEMERIDES+++', self._make_ephemerides()) \
            .replace('+++GRAPH_LABEL_HOURS+++', _('hours')) \
            .replace('+++MOON-PHASE-GRAPHICS+++', moon_phase_graphics) \
            .replace('+++CURRENT-MOON-PHASE-TITLE+++', _('Moon phase:')) \
            .replace('+++CURRENT-MOON-PHASE+++', self.moon_phase.get_phase()) \
            .replace('+++SECTION-EVENTS+++', _('Expected events')) \
            .replace('+++EVENTS+++', self._make_events())

        for aster in ASTERS:
            document = document.replace('+++ASTER_%s+++' % aster.skyfield_name.upper().split(' ')[0],
                                        aster.name)

        return document

    def _make_ephemerides(self) -> str:
        latex = []
        graph_y_component = 18

        if self.ephemerides is not None:
            for ephemeris in self.ephemerides:
                if ephemeris.rise_time is not None:
                    time_fmt = TIME_FORMAT if ephemeris.rise_time.day == self.date.day else SHORT_DATETIME_FORMAT
                    aster_rise = ephemeris.rise_time.strftime(time_fmt)
                else:
                    aster_rise = '-'

                if ephemeris.culmination_time is not None:
                    time_fmt = TIME_FORMAT if ephemeris.culmination_time.day == self.date.day\
                        else SHORT_DATETIME_FORMAT
                    aster_culmination = ephemeris.culmination_time.strftime(time_fmt)
                else:
                    aster_culmination = '-'

                if ephemeris.set_time is not None:
                    time_fmt = TIME_FORMAT if ephemeris.set_time.day == self.date.day else SHORT_DATETIME_FORMAT
                    aster_set = ephemeris.set_time.strftime(time_fmt)
                else:
                    aster_set = '-'

                if not self.show_graph:
                    latex.append(r'\object{%s}{%s}{%s}{%s}' % (ephemeris.object.name,
                                                               aster_rise,
                                                               aster_culmination,
                                                               aster_set))
                else:
                    if ephemeris.rise_time is not None:
                        raise_hour = ephemeris.rise_time.hour
                        raise_minute = ephemeris.rise_time.minute
                    else:
                        raise_hour = raise_minute = 0
                        aster_rise = ''

                    if ephemeris.set_time is not None:
                        set_hour = ephemeris.set_time.hour
                        set_minute = ephemeris.set_time.minute
                    else:
                        set_hour = 24
                        set_minute = 0
                        aster_set = ''
                    sets_after_end = set_hour > raise_hour

                    if not sets_after_end:
                        latex.append(r'\graphobject{%d}{gray}{0}{0}{%d}{%d}{}{%s}' % (graph_y_component,
                                                                                      set_hour,
                                                                                      set_minute,
                                                                                      aster_set))
                        set_hour = 24
                        set_minute = 0

                    latex.append(r'\graphobject{%d}{gray}{%d}{%d}{%d}{%d}{%s}{%s}' % (
                        graph_y_component,
                        raise_hour,
                        raise_minute,
                        set_hour,
                        set_minute,
                        aster_rise,
                        aster_set if sets_after_end else ''
                    ))
                    graph_y_component -= 2

        return ''.join(latex)

    def _make_events(self) -> str:
        latex = []

        for event in self.events:
            latex.append(r'\event{%s}{%s}' % (event.start_time.strftime(TIME_FORMAT),
                                              event.get_description()))

        return ''.join(latex)

    @staticmethod
    def _remove_section(document: str, section: str):
        begin_section_tag = '%%%%%% BEGIN-%s-SECTION' % section.upper()
        end_section_tag = '%%%%%% END-%s-SECTION' % section.upper()

        document = document.split('\n')
        new_document = []

        ignore_line = False
        for line in document:
            if begin_section_tag in line or end_section_tag in line:
                ignore_line = not ignore_line
                continue
            if ignore_line:
                continue
            new_document.append(line)

        return '\n'.join(new_document)


class PdfDumper(Dumper):
    def _convert_dates_to_timezones(self):
        """This method is disabled in this dumper, because the timezone is already converted
         in :class:`_LatexDumper`."""

    def to_string(self):
        try:
            latex_dumper = _LatexDumper(self.ephemerides, self.moon_phase, self.events,
                                        date=self.date, timezone=self.timezone, with_colors=self.with_colors,
                                        show_graph=self.show_graph)
            return self._compile(latex_dumper.to_string())
        except RuntimeError:
            raise UnavailableFeatureError(_("Building PDFs was not possible, because some dependencies are not"
                                            " installed.\nPlease look at the documentation at http://kosmorro.space "
                                            "for more information."))

    @staticmethod
    def is_file_output_needed() -> bool:
        return True

    @staticmethod
    def _compile(latex_input) -> bytes:
        if build_pdf is None:
            raise RuntimeError('Python latex module not found')

        package = str(Path(__file__).parent.absolute()) + '/assets/pdf/'

        return bytes(build_pdf(latex_input, [package]))
