#!/usr/bin/env python3

from .utils import (
    execute,
    KOSMORRO,
)


def check_command_return(result):
    assert result.is_successful()
    assert (
        result.stdout
        == """Monday January 27, 2020

Object     Rise time    Culmination time    Set time
--------  -----------  ------------------  ----------
Sun          07:31           12:01           16:30
Moon         09:06           14:09           19:13
Mercury      08:10           12:49           17:28
Venus        09:01           14:35           20:10
Mars         04:19           08:23           12:28
Jupiter      06:15           10:18           14:21
Saturn       06:56           11:09           15:22
Uranus       10:21           17:25           00:33
Neptune      09:01           14:36           20:10
Pluto        06:57           11:04           15:11

Moon phase: New Moon
First Quarter on Sunday February 02, 2020 at 01:41

Expected events:
20:00  Venus and Neptune are in conjunction

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
