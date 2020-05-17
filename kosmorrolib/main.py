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

import argparse
import locale
import re
import sys

from datetime import date
from termcolor import colored

from . import dumper
from . import core
from . import events

from .data import Position, EARTH
from .exceptions import UnavailableFeatureError
from .i18n import _
from . import ephemerides
from .version import VERSION


def main():
    environment = core.get_env()
    output_formats = get_dumpers()
    args = get_args(list(output_formats.keys()))
    output_format = args.format

    if args.special_action is not None:
        return 0 if args.special_action() else 1

    try:
        compute_date = core.get_date(args.date)
    except ValueError as error:
        print(colored(error.args[0], color='red', attrs=['bold']))
        return -1

    position = None

    if args.latitude is not None or args.longitude is not None:
        position = Position(args.latitude, args.longitude, EARTH)
    elif environment.latitude is not None and environment.longitude is not None:
        position = Position(float(environment.latitude), float(environment.longitude), EARTH)

    if output_format == 'pdf':
        print(_('Save the planet and paper!\n'
                'Consider printing you PDF document only if really necessary, and use the other side of the sheet.'))
        if position is None:
            print()
            print(colored(_("PDF output will not contain the ephemerides, because you didn't provide the observation "
                            "coordinate."), 'yellow'))

    try:
        eph = ephemerides.get_ephemerides(date=compute_date, position=position) if position is not None else None
        moon_phase = ephemerides.get_moon_phase(compute_date)

        events_list = events.search_events(compute_date)

        timezone = args.timezone

        if timezone is None and environment.timezone is not None:
            timezone = int(environment.timezone)
        elif timezone is None:
            timezone = 0

        format_dumper = output_formats[output_format](ephemerides=eph, moon_phase=moon_phase, events=events_list,
                                                      date=compute_date, timezone=timezone, with_colors=args.colors,
                                                      show_graph=args.show_graph)
        output = format_dumper.to_string()
    except UnavailableFeatureError as error:
        print(colored(error.msg, 'red'))
        return 2

    if args.output is not None:
        try:
            with open(args.output, 'wb') as output_file:
                output_file.write(output)
        except OSError as error:
            print(_('Could not save the output in "{path}": {error}').format(path=args.output,
                                                                             error=error.strerror))
    elif not format_dumper.is_file_output_needed():
        print(output)
    else:
        print(colored(_('Selected output format needs an output file (--output).'), color='red'))
        return 1

    return 0


def get_dumpers() -> {str: dumper.Dumper}:
    return {
        'text': dumper.TextDumper,
        'json': dumper.JsonDumper,
        'pdf': dumper.PdfDumper,
    }


def output_version() -> bool:
    python_version = '%d.%d.%d' % (sys.version_info[0], sys.version_info[1], sys.version_info[2])
    print('Kosmorro %s' % VERSION)
    print(_('Running on Python {python_version}').format(python_version=python_version))

    return True


def clear_cache() -> bool:
    confirm = input(_("Do you really want to clear Kosmorro's cache? [yN] ")).upper()
    if re.match(locale.nl_langinfo(locale.YESEXPR), confirm) is not None:
        try:
            core.clear_cache()
        except FileNotFoundError:
            pass
    elif confirm != '' and re.match(locale.nl_langinfo(locale.NOEXPR), confirm) is None:
        print(_('Answer did not match expected options, cache not cleared.'))
        return False

    return True


def get_args(output_formats: [str]):
    today = date.today()

    parser = argparse.ArgumentParser(description=_('Compute the ephemerides and the events for a given date,'
                                                   ' at a given position on Earth.'),
                                     epilog=_('By default, only the events will be computed for today ({date}).\n'
                                              'To compute also the ephemerides, latitude and longitude arguments'
                                              ' are needed.').format(date=today.strftime(dumper.FULL_DATE_FORMAT)))

    parser.add_argument('--version', '-v', dest='special_action', action='store_const', const=output_version,
                        default=None, help=_('Show the program version'))
    parser.add_argument('--clear-cache', dest='special_action', action='store_const', const=clear_cache, default=None,
                        help=_('Delete all the files Kosmorro stored in the cache.'))
    parser.add_argument('--format', '-f', type=str, default=output_formats[0], choices=output_formats,
                        help=_('The format under which the information have to be output'))
    parser.add_argument('--latitude', '-lat', type=float, default=None,
                        help=_("The observer's latitude on Earth. Can also be set in the KOSMORRO_LATITUDE environment "
                               "variable."))
    parser.add_argument('--longitude', '-lon', type=float, default=None,
                        help=_("The observer's longitude on Earth. Can also be set in the KOSMORRO_LONGITUDE "
                               "environment variable."))
    parser.add_argument('--date', '-d', type=str, default=today.strftime('%Y-%m-%d'),
                        help=_('The date for which the ephemerides must be computed (in the YYYY-MM-DD format), '
                               'or as an interval in the "[+-]YyMmDd" format (with Y, M, and D numbers). '
                               'Defaults to the current date ({default_date})').format(
                                   default_date=today.strftime('%Y-%m-%d')))
    parser.add_argument('--timezone', '-t', type=int, default=None,
                        help=_('The timezone to display the hours in (e.g. 2 for UTC+2 or -3 for UTC-3). '
                               'Can also be set in the KOSMORRO_TIMEZONE environment variable.'))
    parser.add_argument('--no-colors', dest='colors', action='store_false',
                        help=_('Disable the colors in the console.'))
    parser.add_argument('--output', '-o', type=str, default=None,
                        help=_('A file to export the output to. If not given, the standard output is used. '
                               'This argument is needed for PDF format.'))
    parser.add_argument('--no-graph', dest='show_graph', action='store_false',
                        help=_('Do not generate a graph to represent the rise and set times in the PDF format.'))

    return parser.parse_args()
