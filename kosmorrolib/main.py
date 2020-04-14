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
from dateutil.relativedelta import relativedelta
from termcolor import colored

from kosmorrolib.version import VERSION
from kosmorrolib import dumper
from kosmorrolib import core
from kosmorrolib import events
from kosmorrolib.i18n import _
from .ephemerides import EphemeridesComputer, Position
from .exceptions import UnavailableFeatureError


def main():
    environment = core.get_env()
    output_formats = get_dumpers()
    args = get_args(list(output_formats.keys()))

    if args.special_action is not None:
        return 0 if args.special_action() else 1

    try:
        compute_date = get_date(args.date)
    except ValueError as error:
        print(colored(error.args[0], color='red', attrs=['bold']))
        return -1

    position = None

    if args.latitude is not None or args.longitude is not None:
        position = Position(args.latitude, args.longitude)
    elif environment.latitude is not None and environment.longitude is not None:
        position = Position(float(environment.latitude), float(environment.longitude))

    if args.format == 'pdf':
        print(_('Save the planet and paper!\n'
                'Consider printing you PDF document only if really necessary, and use the other side of the sheet.'))
        if position is None:
            print()
            print(colored(_("PDF output will not contain the ephemerides, because you didn't provide the observation "
                            "coordinate."), 'yellow'))

    try:
        ephemeris = EphemeridesComputer(position)
        ephemerides = ephemeris.compute_ephemerides(compute_date)

        events_list = events.search_events(compute_date)

        timezone = args.timezone

        if timezone is None and environment.timezone is not None:
            timezone = int(environment.timezone)
        elif timezone is None:
            timezone = 0

        selected_dumper = output_formats[args.format](ephemerides, events_list,
                                                      date=compute_date, timezone=timezone,
                                                      with_colors=args.colors)
        output = selected_dumper.to_string()
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
        print(output)
    else:
        print(colored(_('Selected output format needs an output file (--output).'), color='red'))
        return 1

    return 0


def get_date(date_arg: str) -> date:
    if re.match(r'^\d{4}-\d{2}-\d{2}$', date_arg):
        try:
            return date.fromisoformat(date_arg)
        except ValueError as error:
            raise ValueError(_('The date {date} is not valid: {error}').format(date=date_arg, error=error.args[0]))
    elif re.match(r'^([+-])(([0-9]+)y)?[ ]?(([0-9]+)m)?[ ]?(([0-9]+)d)?$', date_arg):
        def get_offset(date_arg: str, signifier: str):
            if re.search(r'([0-9]+)' + signifier, date_arg):
                return int(re.search(r'[+-]?([0-9]+)' + signifier, date_arg).group(0)[:-1])
            else:
                return 0

        days = get_offset(date_arg, 'd')
        months = get_offset(date_arg, 'm')
        years = get_offset(date_arg, 'y')


        if date_arg[0] == '+':
            return date.today() + relativedelta(days=days, months=months, years=years)
        else:
            return date.today() - relativedelta(days=days, months=months, years=years)

    else:
        raise ValueError(_('The date {date} does not match the required YYYY-MM-DD format or the offset format.').format(date=date_arg))



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
                        help=_("The observer's latitude on Earth. Can also be set in the KOSMORRO_LATITUDE environment "
                               "variable."))
    parser.add_argument('--longitude', '-lon', type=float, default=None,
                        help=_("The observer's longitude on Earth. Can also be set in the KOSMORRO_LONGITUDE "
                               "environment variable."))
    parser.add_argument('--date', '-d', type=str, default=today.strftime('%Y-%m-%d'),
                        help=_('The date for which the ephemerides must be computed (in the YYYY-MM-DD format). '
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

    return parser.parse_args()
