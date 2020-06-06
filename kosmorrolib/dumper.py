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
from termcolor import colored
from .data import ASTERS, AsterEphemerides, MoonPhase, Event
from .i18n import _, FULL_DATE_FORMAT, SHORT_DATETIME_FORMAT, TIME_FORMAT
from .version import VERSION
from .exceptions import UnavailableFeatureError
try:
    from latex import build_pdf
except ImportError:
    build_pdf = None


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

    def get_date_as_string(self, capitalized: bool = False) -> str:
        date = self.date.strftime(FULL_DATE_FORMAT)

        if capitalized:
            return ''.join([date[0].upper(), date[1:]])

        return date

    def __str__(self):
        return self.to_string()

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
        if moon_phase is None:
            return _('Moon phase is unavailable for this date.')

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

        if self.moon_phase is None:
            self.moon_phase = MoonPhase('UNKNOWN')

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
