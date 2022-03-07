#!/usr/bin/env python3

from .utils import (
    execute,
    KOSMORRO,
)


def check_command_return(result):
    assert result.is_successful()
    assert (
        result.stdout
        == """Monday, January 27, 2020

Object     Rise time    Culmination time    Set time
--------  -----------  ------------------  ----------
Sun         7:31 AM         12:01 PM        4:30 PM
Moon        9:06 AM         2:09 PM         7:13 PM
Mercury     8:10 AM         12:49 PM        5:28 PM
Venus       9:01 AM         2:35 PM         8:10 PM
Mars        4:19 AM         8:23 AM         12:28 PM
Jupiter     6:15 AM         10:18 AM        2:21 PM
Saturn      6:56 AM         11:09 AM        3:22 PM
Uranus     10:21 AM         5:25 PM         12:33 AM
Neptune     9:01 AM         2:36 PM         8:10 PM
Pluto       6:57 AM         11:04 AM        3:11 PM

Moon phase: New Moon
First Quarter on Sunday, February 2, 2020 at 1:41 AM

Expected events:
8:00 PM  Venus and Neptune are in conjunction

Note: All the hours are given in UTC.
"""
    )


def test_with_position():
    result = execute(
        KOSMORRO + ["--latitude=50.5876", "--longitude=3.0624", "-d2020-01-27"]
    )
    check_command_return(result)


def test_with_position_env_vars():
    check_command_return(
        execute(
            KOSMORRO + ["-d2020-01-27"],
            environment={
                "KOSMORRO_LATITUDE": "50.5876",
                "KOSMORRO_LONGITUDE": "3.0624",
            },
        )
    )
