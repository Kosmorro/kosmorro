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
import datetime
import sys
import os.path

import pytz
from babel.dates import format_date
from kosmorrolib import Position, get_ephemerides, get_events, get_moon_phase
from kosmorrolib.exceptions import OutOfRangeDateError
from datetime import date

from pytz import timezone

from . import dumper, environment, debug
from .date import parse_date
from .geolocation import get_position
from .utils import (
    KOSMORRO_VERSION,
    KOSMORROLIB_VERSION,
    colored,
    set_colors_activated,
    print_stderr,
    get_timezone,
)
from .exceptions import (
    InvalidOutputFormatError,
    UnavailableFeatureError,
    OutOfRangeDateError as DateRangeError,
)
from kosmorro.i18n.utils import _


def run():
    env_vars = environment.get_env_vars()
    output_formats = get_dumpers()
    args = get_args(list(output_formats.keys()))
    debug.show_debug_messages = args.show_debug_messages
    output_format = args.format

    set_colors_activated(args.colors)

    if args.special_action is not None:
        return 0 if args.special_action() else 1

    try:
        compute_date = parse_date(args.date)
    except ValueError as error:
        print_stderr(colored(error.args[0], color="red", attrs=["bold"]))
        return -1

    position = None
    if args.position not in [None, ""]:
        position = get_position(args.position)
    elif env_vars.position not in [None, ""]:
        position = get_position(env_vars.position)

    # if output format is not specified, try to use output file extension as output format
    if args.output is not None and output_format is None:
        file_extension = os.path.splitext(args.output)[-1][1:].lower()
        if file_extension:
            output_format = file_extension

    # default to .txt if output format was not given and output file did not have file extension
    if output_format is None:
        output_format = "txt"

    if output_format == "tex" and position is None:
        print_stderr(
            colored(
                _(
                    "Output file will not contain the ephemerides, because you didn't provide the observation "
                    "coordinates."
                ),
                "yellow",
            )
        )

    timezone = 0

    try:
        if args.timezone is not None:
            timezone = get_timezone(args.timezone)
        elif env_vars.tz is not None:
            timezone = get_timezone(env_vars.tz)
        elif env_vars.timezone is not None:
            print_stderr(
                colored(
                    _(
                        "Environment variable KOSMORRO_TIMEZONE is deprecated. Use TZ instead, which is more standard."
                    ),
                    "yellow",
                )
            )
            timezone = get_timezone(env_vars.timezone)
    except pytz.UnknownTimeZoneError as error:
        print_stderr(
            colored(
                _("Unknown timezone: {timezone}").format(timezone=error.args[0]),
                color="red",
            )
        )
        return -1

    try:
        use_colors = not environment.NO_COLOR and args.colors

        output = get_information(
            compute_date,
            position,
            timezone,
            output_format,
            use_colors,
            args.show_graph,
        )
    except InvalidOutputFormatError as error:
        print_stderr(colored(error.msg, "red"))
        debug.debug_print(error)
        return 3
    except UnavailableFeatureError as error:
        print_stderr(colored(error.msg, "red"))
        debug.debug_print(error)
        return 2
    except DateRangeError as error:
        print_stderr(colored(error.msg, "red"))
        debug.debug_print(error)
        return 1

    if args.output is not None:
        try:
            file_content = output.to_string()
            opening_mode = get_opening_mode(output_format)
            with open(args.output, opening_mode) as output_file:
                output_file.write(file_content)
        except UnavailableFeatureError as error:
            print_stderr(colored(error.msg, "red"))
            debug.debug_print(error)
            return 2
        except OSError as error:
            print_stderr(
                colored(
                    _('The file could not be saved in "{path}": {error}').format(
                        path=args.output, error=error.strerror
                    ),
                    "red",
                )
            )
            debug.debug_print(error)

            return 3
    elif not output.is_file_output_needed():
        print(output)
    else:
        print_stderr(
            colored(
                _("Please provide a file path to export in this format (--output)."),
                color="red",
            )
        )
        return 1

    return 0


def get_information(
    compute_date: date,
    position: Position,
    timezone: int,
    output_format: str,
    colors: bool,
    show_graph: bool,
) -> dumper.Dumper:
    try:
        if position is not None:
            eph = get_ephemerides(
                for_date=compute_date, position=position, timezone=timezone
            )
        else:
            eph = []

        try:
            moon_phase = get_moon_phase(for_date=compute_date, timezone=timezone)
        except OutOfRangeDateError as error:
            moon_phase = None
            print_stderr(
                colored(
                    _(
                        "Moon phase can only be computed between {min_date} and {max_date}"
                    ).format(
                        min_date=format_date(error.min_date, "long"),
                        max_date=format_date(error.max_date, "long"),
                    ),
                    "yellow",
                )
            )

        events_list = get_events(compute_date, timezone)

        return get_dumpers()[output_format](
            ephemerides=eph,
            moon_phase=moon_phase,
            events=events_list,
            date=compute_date,
            timezone=timezone,
            with_colors=colors,
            show_graph=show_graph,
        )
    except KeyError as error:
        raise InvalidOutputFormatError(output_format, list(get_dumpers().keys()))
    except OutOfRangeDateError as error:
        raise DateRangeError(error.min_date, error.max_date)


def get_dumpers() -> {str: dumper.Dumper}:
    return {
        "txt": dumper.TextDumper,
        "json": dumper.JsonDumper,
        "tex": dumper.LatexDumper,
    }


def get_opening_mode(format: str) -> str:
    return "w"


def output_version() -> bool:
    python_version = "%d.%d.%d" % (
        sys.version_info[0],
        sys.version_info[1],
        sys.version_info[2],
    )
    print("Kosmorro %s" % KOSMORRO_VERSION)
    print(
        _(
            "Running on Python {python_version} "
            "with Kosmorrolib v{kosmorrolib_version}"
        ).format(python_version=python_version, kosmorrolib_version=KOSMORROLIB_VERSION)
    )

    return True


def get_args(output_formats: [str]):
    today = date.today()

    parser = argparse.ArgumentParser(
        description=_(
            "Compute the ephemerides and the events for a given date and a given position on Earth."
        ),
        epilog=_(
            "By default, only the events will be computed for today.\n"
            "To compute also the ephemerides, latitude and longitude arguments are needed."
        ),
    )

    parser.add_argument(
        "--version",
        "-v",
        dest="special_action",
        action="store_const",
        const=output_version,
        default=None,
        help=_("Show the program version"),
    )
    parser.add_argument(
        "--format",
        "-f",
        type=str,
        default=None,
        choices=output_formats,
        help=_(
            "The format to output the information to. If not provided, the output format "
            "will be inferred from the file extension of the output file."
        ),
    )
    parser.add_argument(
        "--position",
        "-p",
        type=str,
        default=None,
        help=_(
            'The observer\'s position on Earth, in the "{latitude},{longitude}" format. '
            "Can also be set in the KOSMORRO_POSITION environment variable."
        ),
    )
    parser.add_argument(
        "--date",
        "-d",
        type=str,
        default=today.strftime("%Y-%m-%d"),
        help=_(
            "The date for which the ephemerides must be calculated. Can be in the YYYY-MM-DD format "
            'or an interval in the "[+-]YyMmDd" format (with Y, M, and D numbers). '
            "Defaults to current date."
        ).format(default_date=today.strftime("%Y-%m-%d")),
    )
    parser.add_argument(
        "--timezone",
        "-t",
        type=str,
        default=None,
        help=_(
            "The timezone to use to display the hours. It can be either a number (e.g. 1 for UTC+1) or a timezone name (e.g. Europe/Paris). "
            "See https://en.wikipedia.org/wiki/List_of_tz_database_time_zones to find your timezone. "
            "Can also be set in the TZ environment variable."
        ),
    )
    parser.add_argument(
        "--no-colors",
        dest="colors",
        action="store_false",
        help=_("Disable the colors in the console."),
    )
    parser.add_argument(
        "--output",
        "-o",
        type=str,
        default=None,
        help=_(
            "A file to export the output to. If not given, the standard output is used."
        ),
    )
    parser.add_argument(
        "--no-graph",
        dest="show_graph",
        action="store_false",
        help=_(
            "Do not generate a graph to represent the rise and set times in the LaTeX file."
        ),
    )
    parser.add_argument(
        "--debug",
        dest="show_debug_messages",
        action="store_true",
        help=_("Show debugging messages"),
    )

    return parser.parse_args()


def main():
    sys.exit(run())
