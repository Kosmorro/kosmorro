#!/usr/bin/env python3

from sys import version_info as python_version
from .utils import (
    execute,
    KOSMORRO,
    CURRENT_MOON_PHASE_PATTERN,
    NEXT_MOON_PHASE_PATTERN,
)
from datetime import date
from babel.dates import format_date


def test_run_without_argument():
    result = execute(KOSMORRO)
    assert result.successful

    stdout = result.stdout.split("\n")
    print(stdout)

    # It always starts with the current date, an empty line and the current and next Moon date:
    assert stdout[0] == format_date(date.today(), "full", "EN")
    assert stdout[1] == ""
    assert CURRENT_MOON_PHASE_PATTERN.match(stdout[2])
    assert NEXT_MOON_PHASE_PATTERN.match(stdout[3])

    # It always finishes with an empty line, a note about UTC timezone and an empty line:
    assert stdout[-3] == ""
    assert stdout[-2] == "Note: All the hours are given in UTC."
    assert stdout[-1] == ""


def test_help_message():
    for arg in ["--help", "-h"]:
        result = execute(KOSMORRO + [arg])

        assert result.successful

        if python_version.major == 3 and python_version.minor < 13:
            assert (
                result.stdout
                == """usage: kosmorro [-h] [--version] [--format {txt,json,tex}]
                [--position POSITION] [--date DATE] [--timezone TIMEZONE]
                [--no-colors] [--output OUTPUT] [--no-graph] [--debug]
                [--completion COMPLETION]

Compute the ephemerides and the events for a given date and a given position
on Earth.

options:
  -h, --help            show this help message and exit
  --version, -v         Show the program version
  --format {txt,json,tex}, -f {txt,json,tex}
                        The format to output the information to. If not
                        provided, the output format will be inferred from the
                        file extension of the output file.
  --position POSITION, -p POSITION
                        The observer's position on Earth, in the
                        "{latitude},{longitude}" format. Can also be set in
                        the KOSMORRO_POSITION environment variable.
  --date DATE, -d DATE  The date for which the ephemerides must be calculated.
                        Can be in the YYYY-MM-DD format or an interval in the
                        "[+-]YyMmDd" format (with Y, M, and D numbers).
                        Defaults to current date.
  --timezone TIMEZONE, -t TIMEZONE
                        The timezone to use to display the hours. It can be
                        either a number (e.g. 1 for UTC+1) or a timezone name
                        (e.g. Europe/Paris). See https://en.wikipedia.org/wiki
                        /List_of_tz_database_time_zones to find your timezone.
                        Can also be set in the TZ environment variable.
  --no-colors           Disable the colors in the console.
  --output OUTPUT, -o OUTPUT
                        A file to export the output to. If not given, the
                        standard output is used.
  --no-graph            Do not generate a graph to represent the rise and set
                        times in the LaTeX file.
  --debug               Show debugging messages
  --completion COMPLETION
                        Print a script allowing completion for your shell

By default, only the events will be computed for today. To compute also the
ephemerides, latitude and longitude arguments are needed.
"""
            )
        else:
            assert (
                result.stdout
                == """usage: kosmorro [-h] [--version] [--format {txt,json,tex}]
                [--position POSITION] [--date DATE] [--timezone TIMEZONE]
                [--no-colors] [--output OUTPUT] [--no-graph] [--debug]
                [--completion COMPLETION]

Compute the ephemerides and the events for a given date and a given position
on Earth.

options:
  -h, --help            show this help message and exit
  --version, -v         Show the program version
  --format, -f {txt,json,tex}
                        The format to output the information to. If not
                        provided, the output format will be inferred from the
                        file extension of the output file.
  --position, -p POSITION
                        The observer's position on Earth, in the
                        "{latitude},{longitude}" format. Can also be set in
                        the KOSMORRO_POSITION environment variable.
  --date, -d DATE       The date for which the ephemerides must be calculated.
                        Can be in the YYYY-MM-DD format or an interval in the
                        "[+-]YyMmDd" format (with Y, M, and D numbers).
                        Defaults to current date.
  --timezone, -t TIMEZONE
                        The timezone to use to display the hours. It can be
                        either a number (e.g. 1 for UTC+1) or a timezone name
                        (e.g. Europe/Paris). See https://en.wikipedia.org/wiki
                        /List_of_tz_database_time_zones to find your timezone.
                        Can also be set in the TZ environment variable.
  --no-colors           Disable the colors in the console.
  --output, -o OUTPUT   A file to export the output to. If not given, the
                        standard output is used.
  --no-graph            Do not generate a graph to represent the rise and set
                        times in the LaTeX file.
  --debug               Show debugging messages
  --completion COMPLETION
                        Print a script allowing completion for your shell

By default, only the events will be computed for today. To compute also the
ephemerides, latitude and longitude arguments are needed.
"""
            )
