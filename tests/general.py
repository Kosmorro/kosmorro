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
