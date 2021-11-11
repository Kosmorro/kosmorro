#!/usr/bin/env python3

import aurornis
import re

from os import environ
from typing import Union

DEFAULT_ENVIRONMENT = {"PATH": environ["PATH"]}
KOSMORRO = ["./kosmorro", "--no-color"]

CURRENT_MOON_PHASE_PATTERN = re.compile(
    r"^Moon phase: ("
    r"(New Moon)|(Waxing Crescent)|"
    r"(First Quarter)|(Waxing Gibbous)|"
    r"(Full Moon)|(Waning Gibbous)|"
    r"(Last Quarter)|(Waning Crescent)"
    r")$"
)

NEXT_MOON_PHASE_PATTERN = re.compile(
    r"^((New Moon)|(Waxing Crescent)|"
    r"(First Quarter)|(Waxing Gibbous)|"
    r"(Full Moon)|(Waning Gibbous)|"
    r"(Last Quarter)|(Waning Crescent)"
    r") "
    r"on ((Monday)|(Tuesday)|(Wednesday)|(Thursday)|(Friday)|(Saturday)|(Sunday)) "
    r"((January)|(February)|(March)|(April)|(May)|(June)|"
    r"(July)|(August)|(September)|(October)|(November)|(December)) "
    r"[0-9]{2}, [0-9]{4} at [0-9]{2}:[0-9]{2}$"
)


def execute(
    command, environment: {str: Union[int, str]} = None
) -> aurornis.CommandResult:
    if environment is None:
        environment = DEFAULT_ENVIRONMENT
    else:
        for variable in DEFAULT_ENVIRONMENT:
            environment[variable] = DEFAULT_ENVIRONMENT[variable]

    return aurornis.run(command, environment)


def assert_nb_lines(expected_nb: int, in_str: str):
    """Check that the string has the specified number of lines and that the last one is empty."""
    lines = in_str.split("\n")
    assert len(lines) == expected_nb
    assert lines[len(lines) - 1] == ""
