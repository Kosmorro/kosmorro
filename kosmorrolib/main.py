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

from datetime import date, timedelta
from termcolor import colored

from kosmorrolib.version import VERSION
from kosmorrolib import dumper
from kosmorrolib import core
from kosmorrolib import events
from kosmorrolib.i18n import _
from .ephemerides import EphemeridesComputer, Position
from .exceptions import UnavailableFeatureError


def main():
    output_formats = get_dumpers()
    args = get_args(list(output_formats.keys()))

    if args.special_action is not None:
        return 0 if args.special_action() else 1

    try:
        if args.until_date is None:
            from_date = get_date(args.date)
            until_date = from_date
        else:
            until_date = get_date(args.until_date)
            from_date = get_date(args.from_date) if args.from_date is not None else date.today()
    except ValueError as error:
        print(colored(error.args[0], color='red', attrs=['bold']))
        return -1

    if args.latitude is None or args.longitude is None:
        position = None
    else:
        position = Position(args.latitude, args.longitude)

    if args.format == 'pdf':
        print(_('Save the planet and paper!\n'
                'Consider printing you PDF document only if really necessary, and use the other side of the sheet.'))
        if position is None:
            print()
            print(colored(_("PDF output will not contain the ephemerides, because you didn't provide the observation "
                            "coordinate."), 'yellow'))

    try:
        compute_date = from_date
        selected_dumper = output_formats[args.format](None, None, date=None, timezone=args.timezone,
                                                      with_colors=args.colors)
        ephemeris = EphemeridesComputer(position)

        output = []
        while compute_date <= until_date:
            ephemerides = ephemeris.compute_ephemerides(compute_date)
            events_list = events.search_events(compute_date)

            selected_dumper.date = compute_date
            selected_dumper.ephemeris = ephemerides
            selected_dumper.events = events_list

            output.append(selected_dumper.to_string())

            compute_date = compute_date + timedelta(days=1)

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
    elif not selected_dumper.is_file_output_needed():
        print('\n\n'.join(output))
    else:
        print(colored(_('Selected output format needs an output file (--output).'), color='red'))
        return 1

    return 0


def get_date(yyyymmdd: str) -> date:
    if not re.match(r'^\d{4}-\d{2}-\d{2}$', yyyymmdd):
        raise ValueError(_('The date {date} does not match the required YYYY-MM-DD format.').format(date=yyyymmdd))

    try:
        return date.fromisoformat(yyyymmdd)
    except ValueError as error:
        raise ValueError(_('The date {date} is not valid: {error}').format(date=yyyymmdd, error=error.args[0]))


def get_dumpers() -> {str: dumper.Dumper}:
    return {
        'text': dumper.TextDumper,
        'json': dumper.JsonDumper,
        'pdf': dumper.PdfDumper
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
                        help=_("The observer's latitude on Earth"))
    parser.add_argument('--longitude', '-lon', type=float, default=None,
                        help=_("The observer's longitude on Earth"))
    parser.add_argument('--date', '-d', type=str, default=today.strftime('%Y-%m-%d'),
                        help=_('The date for which the ephemerides must be computed (in the YYYY-MM-DD format). '
                               'Defaults to the current date ({default_date}). Ignored if the --from and --to are '
                               'used.').format(default_date=today.strftime('%Y-%m-%d')))
    parser.add_argument('--from', type=str, default=None, dest='from_date',
                        help=_('The first of the set of dates the computations must be done for. If this argument '
                               'is set, then the --until argument is mandatory. Defaults to the current date if only '
                               'the --until argument is set.'))
    parser.add_argument('--until', type=str, default=None, dest='until_date',
                        help=_('The last of the set of dates the computations must be done for. Mandatory '
                               'if the --from argument is set, then this argument is mandatory.'))
    parser.add_argument('--timezone', '-t', type=int, default=0,
                        help=_('The timezone to display the hours in (e.g. 2 for UTC+2 or -3 for UTC-3).'))
    parser.add_argument('--no-colors', dest='colors', action='store_false',
                        help=_('Disable the colors in the console.'))
    parser.add_argument('--output', '-o', type=str, default=None,
                        help=_('A file to export the output to. If not given, the standard output is used. '
                               'This argument is needed for PDF format.'))

    return parser.parse_args()
