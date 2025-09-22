#!/usr/bin/env python3

from .utils import (
    execute,
    KOSMORRO,
)


def test_timezone_with_command_line_arg():
    result = execute(KOSMORRO + ["--timezone=1", "-d2020-01-27"])
    assert result.successful
    assert "Note: All the hours are given in the UTC+1.0 timezone." in result.stdout

    result = execute(KOSMORRO + ["--timezone=Europe/Paris", "-d2020-01-27"])
    assert result.successful
    assert "Note: All the hours are given in the UTC+1.0 timezone." not in result.stdout

    result = execute(KOSMORRO + ["--timezone=-5", "-d2020-01-27"])
    assert result.successful
    assert "Note: All the hours are given in the UTC-5.0 timezone." in result.stdout

    result = execute(KOSMORRO + ["--timezone=America/Chicago", "-d2020-01-27"])
    assert result.successful
    assert "Note: All the hours are given in the UTC-5.0 timezone." in result.stdout


def test_timezone_with_env_var():
    result = execute(KOSMORRO + ["-d2020-01-27"], environment={"TZ": "1"})
    assert result.successful
    assert "Note: All the hours are given in the UTC+1.0 timezone." in result.stdout

    result = execute(KOSMORRO + ["-d2020-01-27"], environment={"TZ": "Europe/Paris"})
    assert result.successful
    assert "Note: All the hours are given in the UTC+1.0 timezone." not in result.stdout

    result = execute(KOSMORRO + ["-d2020-01-27"], environment={"TZ": "-5"})
    assert result.successful
    assert "Note: All the hours are given in the UTC-5.0 timezone." in result.stdout

    result = execute(KOSMORRO + ["-d2020-01-27"], environment={"TZ": "America/Chicago"})
    assert result.successful
    assert "Note: All the hours are given in the UTC-5.0 timezone." in result.stdout


def test_timezone_with_env_var_and_command_line_arg():
    result = execute(
        KOSMORRO + ["--timezone=3", "-d2020-01-27"], environment={"TZ": "Europe/Paris"}
    )
    assert result.successful
    assert "Note: All the hours are given in the UTC+3.0 timezone." in result.stdout


def test_timezone_with_deprecated_env_var():
    result = execute(
        KOSMORRO + ["-d2020-01-27"], environment={"KOSMORRO_TIMEZONE": "1"}
    )
    assert result.successful
    assert (
        "Environment variable KOSMORRO_TIMEZONE is deprecated. Use TZ instead, which is more standard."
        in result.stderr
    )
    assert "Note: All the hours are given in the UTC+1.0 timezone." in result.stdout

    result = execute(
        KOSMORRO + ["-d2020-01-27"], environment={"KOSMORRO_TIMEZONE": "Europe/Paris"}
    )
    assert result.successful
    assert (
        "Environment variable KOSMORRO_TIMEZONE is deprecated. Use TZ instead, which is more standard."
        in result.stderr
    )
    assert "Note: All the hours are given in the UTC+1.0 timezone." not in result.stdout

    result = execute(
        KOSMORRO + ["-d2020-01-27"], environment={"KOSMORRO_TIMEZONE": "-5"}
    )
    assert result.successful
    assert (
        "Environment variable KOSMORRO_TIMEZONE is deprecated. Use TZ instead, which is more standard."
        in result.stderr
    )
    assert "Note: All the hours are given in the UTC-5.0 timezone." in result.stdout

    result = execute(
        KOSMORRO + ["-d2020-01-27"],
        environment={"KOSMORRO_TIMEZONE": "America/Chicago"},
    )
    assert result.successful
    assert (
        "Environment variable KOSMORRO_TIMEZONE is deprecated. Use TZ instead, which is more standard."
        in result.stderr
    )
    assert "Note: All the hours are given in the UTC-5.0 timezone." in result.stdout
