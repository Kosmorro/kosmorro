#!/usr/bin/env python3

from sys import version_info
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
    assert result.is_successful()

    stdout = result.stdout.split("\n")
    print(stdout)

    # It always starts with the current date, an empty line and the current and next Moon date:
    assert stdout[0] == format_date(date.today(), "full")
    assert stdout[1] == ""
    assert CURRENT_MOON_PHASE_PATTERN.match(stdout[2])
    assert NEXT_MOON_PHASE_PATTERN.match(stdout[3])

    # It always finishes with an empty line, a note about UTC timezone and an empty line:
    assert stdout[-3] == ""
    assert stdout[-2] == "Note: All the hours are given in UTC."
    assert stdout[-1] == ""


def test_help_message():
    python_version = (version_info.major, version_info.minor)

    for arg in ["--help", "-h"]:
        result = execute(KOSMORRO + [arg])
        assert result.is_successful()

        # Options header has changed from "optional arguments" to "options" in Python 3.10.
        options_header = (
            "options" if python_version == (3, 10) else "optional arguments"
        )

        assert (
            result.stdout
            == """usage: kosmorro [-h] [--version] [--format {text,json,pdf}]
                [--latitude LATITUDE] [--longitude LONGITUDE] [--date DATE]
                [--timezone TIMEZONE] [--no-colors] [--output OUTPUT]
                [--no-graph] [--debug]

Compute the ephemerides and the events for a given date and a given position
on Earth.

%s:
  -h, --help            show this help message and exit
  --version, -v         Show the program version
  --format {text,json,pdf}, -f {text,json,pdf}
                        The format to output the information to
  --latitude LATITUDE, -lat LATITUDE
                        The observer's latitude on Earth. Can also be set in
                        the KOSMORRO_LATITUDE environment variable.
  --longitude LONGITUDE, -lon LONGITUDE
                        The observer's longitude on Earth. Can also be set in
                        the KOSMORRO_LONGITUDE environment variable.
  --date DATE, -d DATE  The date for which the ephemerides must be calculated.
                        Can be in the YYYY-MM-DD format or an interval in the
                        "[+-]YyMmDd" format (with Y, M, and D numbers).
                        Defaults to current date.
  --timezone TIMEZONE, -t TIMEZONE
                        The timezone to display the hours in (e.g. 2 for UTC+2
                        or -3 for UTC-3). Can also be set in the
                        KOSMORRO_TIMEZONE environment variable.
  --no-colors           Disable the colors in the console.
  --output OUTPUT, -o OUTPUT
                        A file to export the output to. If not given, the
                        standard output is used. This argument is needed for
                        PDF format.
  --no-graph            Do not generate a graph to represent the rise and set
                        times in the PDF format.
  --debug               Show debugging messages

By default, only the events will be computed for today. To compute also the
ephemerides, latitude and longitude arguments are needed.
"""
            % options_header
        )
