#!/usr/bin/env python3

from .utils import (
    execute,
    KOSMORRO,
)


def check_command_return_t_plus_one(result):
    assert result.is_successful()
    assert (
        result.stdout
        == """Monday, January 27, 2020

Moon phase: New Moon
First Quarter on Sunday, February 2, 2020 at 2:41 AM

Expected events:
9:00 PM  Venus and Neptune are in conjunction

Note: All the hours are given in the UTC+1 timezone.
"""
    )


def check_command_return_t_minus_one(result):
    assert result.is_successful()
    assert (
        result.stdout
        == """Monday, January 27, 2020

Moon phase: New Moon
First Quarter on Sunday, February 2, 2020 at 12:41 AM

Expected events:
7:00 PM  Venus and Neptune are in conjunction

Note: All the hours are given in the UTC-1 timezone.
"""
    )


def test_timezone():
    check_command_return_t_plus_one(
        execute(KOSMORRO + ["--timezone=1", "-d2020-01-27"])
    )
    check_command_return_t_minus_one(
        execute(KOSMORRO + ["--timezone=-1", "-d2020-01-27"])
    )


def test_timezone_with_env_var():
    check_command_return_t_plus_one(
        execute(KOSMORRO + ["-d2020-01-27"], environment={"KOSMORRO_TIMEZONE": "1"})
    )
    check_command_return_t_minus_one(
        execute(KOSMORRO + ["-d2020-01-27"], environment={"KOSMORRO_TIMEZONE": "-1"})
    )

    # If both environment variable and argument are set, use argument:

    check_command_return_t_plus_one(
        execute(
            KOSMORRO + ["--timezone=1", "-d2020-01-27"],
            environment={"KOSMORRO_TIMEZONE": "-1"},
        )
    )
    check_command_return_t_minus_one(
        execute(
            KOSMORRO + ["--timezone=-1", "-d2020-01-27"],
            environment={"KOSMORRO_TIMEZONE": "1"},
        )
    )
