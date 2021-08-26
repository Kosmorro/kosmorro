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

from kosmorrolib import Position, get_ephemerides, get_events, get_moon_phase
from kosmorrolib.__version__ import __version__ as kosmorrolib_version
from kosmorrolib.exceptions import OutOfRangeDateError
from datetime import date
from termcolor import colored

from . import dumper, environment, debug
from .date import parse_date
from .__version__ import __version__ as kosmorro_version
from .exceptions import UnavailableFeatureError, OutOfRangeDateError as DateRangeError
from _kosmorro.i18n.utils import _, SHORT_DATE_FORMAT


def main():
    env_vars = environment.get_env_vars()
    output_formats = get_dumpers()
    args = get_args(list(output_formats.keys()))
    debug.show_debug_messages = args.show_debug_messages
    output_format = args.format

    if args.special_action is not None:
        return 0 if args.special_action() else 1

    try:
        compute_date = parse_date(args.date)
    except ValueError as error:
        print(colored(error.args[0], color="red", attrs=["bold"]))
        return -1

    position = None

    if args.latitude is not None or args.longitude is not None:
        position = Position(args.latitude, args.longitude)
    elif env_vars.latitude is not None and env_vars.longitude is not None:
        position = Position(float(env_vars.latitude), float(env_vars.longitude))

    if output_format == "pdf":
        print(
            _(
                "Save the planet and paper!\n"
                "Consider printing your PDF document only if really necessary, and use the other side of the sheet."
            )
        )
        if position is None:
            print()
            print(
                colored(
                    _(
                        "PDF output will not contain the ephemerides, because you didn't provide the observation "
                        "coordinates."
                    ),
                    "yellow",
                )
            )

    timezone = args.timezone

    if timezone is None and env_vars.timezone is not None:
        timezone = int(env_vars.timezone)
    elif timezone is None:
        timezone = 0

    try:
        output = get_information(
            compute_date,
            position,
            timezone,
            output_format,
            args.colors,
            args.show_graph,
        )
    except UnavailableFeatureError as error:
        print(colored(error.msg, "red"))
        debug.debug_print(error)
        return 2
    except DateRangeError as error:
        print(colored(error.msg, "red"))
        debug.debug_print(error)
        return 1

    if args.output is not None:
        try:
            pdf_content = output.to_string()
            with open(args.output, "wb") as output_file:
                output_file.write(pdf_content)
        except UnavailableFeatureError as error:
            print(colored(error.msg, "red"))
            debug.debug_print(error)
            return 2
        except OSError as error:
            print(
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
        print(
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
    if position is not None:
        try:
            eph = get_ephemerides(
                date=compute_date, position=position, timezone=timezone
            )
        except OutOfRangeDateError as error:
            raise DateRangeError(error.min_date, error.max_date)
    else:
        eph = []

    try:
        moon_phase = get_moon_phase(compute_date)
    except OutOfRangeDateError as error:
        moon_phase = None
        print(
            colored(
                _(
                    "Moon phase can only be displayed between {min_date} and {max_date}"
                ).format(
                    min_date=error.min_date.strftime(SHORT_DATE_FORMAT),
                    max_date=error.max_date.strftime(SHORT_DATE_FORMAT),
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


def get_dumpers() -> {str: dumper.Dumper}:
    return {
        "text": dumper.TextDumper,
        "json": dumper.JsonDumper,
        "pdf": dumper.PdfDumper,
    }


def output_version() -> bool:
    python_version = "%d.%d.%d" % (
        sys.version_info[0],
        sys.version_info[1],
        sys.version_info[2],
    )
    print("Kosmorro %s" % kosmorro_version)
    print(
        _(
            "Running on Python {python_version} "
            "with Kosmorrolib v{kosmorrolib_version}"
        ).format(python_version=python_version, kosmorrolib_version=kosmorrolib_version)
    )

    return True


def clear_cache() -> bool:
    confirm = input(_("Do you really want to clear Kosmorro's cache? [yN] ")).upper()
    if re.match(locale.nl_langinfo(locale.YESEXPR), confirm) is not None:
        try:
            environment.clear_cache()
        except FileNotFoundError:
            debug.debug_print("No cache found, nothing done.")
            pass
    elif confirm != "" and re.match(locale.nl_langinfo(locale.NOEXPR), confirm) is None:
        print(_("Incorrect answer, cache not cleared."))
        return False

    return True


def get_args(output_formats: [str]):
    today = date.today()

    parser = argparse.ArgumentParser(
        description=_(
            "Compute the ephemerides and the events for a given date and a given position on Earth."
        ),
        epilog=_(
            "By default, only the events will be computed for today ({date}).\n"
            "To compute also the ephemerides, latitude and longitude arguments"
            " are needed."
        ).format(date=today.strftime(dumper.FULL_DATE_FORMAT)),
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
        "--clear-cache",
        dest="special_action",
        action="store_const",
        const=clear_cache,
        default=None,
        help=_("Delete all the files from Kosmorro's cache."),
    )
    parser.add_argument(
        "--format",
        "-f",
        type=str,
        default=output_formats[0],
        choices=output_formats,
        help=_("The format to output the information to"),
    )
    parser.add_argument(
        "--latitude",
        "-lat",
        type=float,
        default=None,
        help=_(
            "The observer's latitude on Earth. Can also be set in the KOSMORRO_LATITUDE environment "
            "variable."
        ),
    )
    parser.add_argument(
        "--longitude",
        "-lon",
        type=float,
        default=None,
        help=_(
            "The observer's longitude on Earth. Can also be set in the KOSMORRO_LONGITUDE "
            "environment variable."
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
            "Defaults to today ({default_date})."
        ).format(default_date=today.strftime("%Y-%m-%d")),
    )
    parser.add_argument(
        "--timezone",
        "-t",
        type=int,
        default=None,
        help=_(
            "The timezone to display the hours in (e.g. 2 for UTC+2 or -3 for UTC-3). "
            "Can also be set in the KOSMORRO_TIMEZONE environment variable."
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
            "A file to export the output to. If not given, the standard output is used. "
            "This argument is needed for PDF format."
        ),
    )
    parser.add_argument(
        "--no-graph",
        dest="show_graph",
        action="store_false",
        help=_(
            "Do not generate a graph to represent the rise and set times in the PDF format."
        ),
    )
    parser.add_argument(
        "--debug",
        dest="show_debug_messages",
        action="store_true",
        help=_("Show debugging messages"),
    )

    return parser.parse_args()
