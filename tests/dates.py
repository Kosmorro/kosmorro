#!/usr/bin/env python3

from .utils import execute, KOSMORRO


def test_with_date():
    for arg in [["-d", "2020-01-27"], ["--date", "2020-01-27"], ["-d2020-01-27"]]:
        result = execute(KOSMORRO + arg)
        assert result.is_successful()

        assert (
            result.stdout
            == """Monday January 27, 2020

Moon phase: New Moon
First Quarter on Sunday February 02, 2020 at 01:41

Expected events:
20:00  Venus and Neptune are in conjunction

Note: All the hours are given in UTC.
"""
        )


def test_with_incorrect_date_values():
    value = "yolo-yo-lo"
    for arg in [["-d", value], ["--date", value], [f"-d{value}"]]:
        result = execute(KOSMORRO + arg)
        assert not result.is_successful()
        assert (
            result.stdout
            == f"The date {value} does not match the required YYYY-MM-DD format or the offset format.\n"
        )

    value = "2020-13-32"
    for arg in [["-d", value], ["--date", value], [f"-d{value}"]]:
        result = execute(KOSMORRO + arg)
        assert not result.is_successful()
        assert (
            result.stdout == f"The date {value} is not valid: month must be in 1..12\n"
        )


def test_with_out_of_range_dates():
    for arg in [["-d", "1789-05-05"], ["-d", "3000-01-01"]]:
        result = execute(KOSMORRO + arg)
        assert not result.is_successful()
        assert (
            result.stdout
            == "Moon phase can only be displayed between Aug 09, 1899 and Sep 26, 2053\n"
        )
