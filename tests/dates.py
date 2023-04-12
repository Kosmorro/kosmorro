#!/usr/bin/env python3

from .utils import execute, KOSMORRO


def test_with_date():
    for arg in [["-d", "2020-01-27"], ["--date", "2020-01-27"], ["-d2020-01-27"]]:
        result = execute(KOSMORRO + arg)
        assert result.is_successful()

        assert (
            result.stdout
            == """Monday, January 27, 2020

Moon phase: New Moon
First Quarter on Sunday, February 2, 2020 at 1:41 AM

Expected events:
8:00 PM  Venus and Neptune are in conjunction

Note: All the hours are given in UTC.
"""
        )


def test_with_incorrect_date_values():
    value = "yolo-yo-lo"
    for arg in [["-d", value], ["--date", value], [f"-d{value}"]]:
        result = execute(KOSMORRO + arg)
        assert not result.is_successful()
        assert (
            result.stderr
            == f"The date {value} does not match the required YYYY-MM-DD format or the offset format.\n"
        )

    value = "2020-13-32"
    for arg in [["-d", value], ["--date", value], [f"-d{value}"]]:
        result = execute(KOSMORRO + arg)
        assert not result.is_successful()
        assert (
            result.stderr == f"The date {value} is not valid: month must be in 1..12\n"
        )


def test_with_out_of_range_dates():
    for arg in [["-d", "1789-05-05"], ["-d", "3000-01-01"]]:
        result = execute(KOSMORRO + arg)
        assert not result.is_successful()
        assert (
            result.stderr
            == "Moon phase can only be computed between August 9, 1899 and September 26, 2053\nThe date must be between July 28, 1899 and October 8, 2053\n"
        )


def test_with_out_of_range_dates_for_moon_phase_only():
    for arg in [["-d", "1899-07-30"], ["-d", "2053-10-06"]]:
        result = execute(KOSMORRO + arg)
        assert result.is_successful()
        assert (
            result.stderr
            == "Moon phase can only be computed between August 9, 1899 and September 26, 2053\n"
        )
