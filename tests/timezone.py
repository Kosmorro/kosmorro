#!/usr/bin/env python3

import pytest

from .utils import (
    execute,
    KOSMORRO,
)


def timezone_with_command_line_arg_input():
    yield [
        "--timezone=1",
        "-d2020-01-27",
    ], "Note: All the hours are given in the UTC+1.0 timezone."
    yield [
        "--timezone=Europe/Paris",
        "-d2020-01-27",
    ], "Note: All the hours are given in the UTC+1.0 timezone."
    # Paris is at UTC+2 in July:
    yield [
        "--timezone=Europe/Paris",
        "-d2020-07-27",
    ], "Note: All the hours are given in the UTC+2.0 timezone."
    yield [
        "--timezone=-5",
        "-d2020-01-27",
    ], "Note: All the hours are given in the UTC-5.0 timezone."
    yield [
        "--timezone=America/Chicago",
        "-d2020-01-27",
    ], "Note: All the hours are given in the UTC-6.0 timezone."
    # Chicago is at UTC+6 in July:
    yield [
        "--timezone=America/Chicago",
        "-d2020-07-27",
    ], "Note: All the hours are given in the UTC-5.0 timezone."


@pytest.mark.parametrize(
    "args, expected_stdout_line", timezone_with_command_line_arg_input()
)
def test_timezone_with_command_line_arg(args, expected_stdout_line):
    result = execute(KOSMORRO + args)
    assert result.successful
    assert expected_stdout_line in result.stdout


def timezone_with_env_var_input():
    yield {"TZ": "1"}, [
        "-d2020-01-27"
    ], "Note: All the hours are given in the UTC+1.0 timezone."
    yield {"TZ": "Europe/Paris"}, [
        "-d2020-01-27"
    ], "Note: All the hours are given in the UTC+1.0 timezone."
    yield {"TZ": "Europe/Paris"}, [
        "-d2020-07-27"
    ], "Note: All the hours are given in the UTC+2.0 timezone."
    yield {"TZ": "-5"}, [
        "-d2020-01-27"
    ], "Note: All the hours are given in the UTC-5.0 timezone."
    yield {"TZ": "America/Chicago"}, [
        "-d2020-01-27"
    ], "Note: All the hours are given in the UTC-6.0 timezone."
    yield {"TZ": "America/Chicago"}, [
        "-d2020-07-27"
    ], "Note: All the hours are given in the UTC-5.0 timezone."


@pytest.mark.parametrize(
    "environment, args, expected_stdout_line", timezone_with_env_var_input()
)
def test_timezone_with_env_var(environment, args, expected_stdout_line):
    result = execute(KOSMORRO + args, environment=environment)
    assert result.successful
    assert expected_stdout_line in result.stdout


def test_timezone_with_env_var_and_command_line_arg():
    result = execute(
        KOSMORRO + ["--timezone=3", "-d2020-01-27"], environment={"TZ": "Europe/Paris"}
    )
    assert result.successful
    assert "Note: All the hours are given in the UTC+3.0 timezone." in result.stdout


def timezone_with_deprecated_env_var_input():
    yield {"KOSMORRO_TIMEZONE": "1"}, [
        "-d2020-01-27"
    ], "Note: All the hours are given in the UTC+1.0 timezone."
    yield {"KOSMORRO_TIMEZONE": "Europe/Paris"}, [
        "-d2020-01-27"
    ], "Note: All the hours are given in the UTC+1.0 timezone."
    yield {"KOSMORRO_TIMEZONE": "Europe/Paris"}, [
        "-d2020-07-27"
    ], "Note: All the hours are given in the UTC+2.0 timezone."
    yield {"KOSMORRO_TIMEZONE": "-5"}, [
        "-d2020-01-27"
    ], "Note: All the hours are given in the UTC-5.0 timezone."
    yield {"KOSMORRO_TIMEZONE": "America/Chicago"}, [
        "-d2020-01-27"
    ], "Note: All the hours are given in the UTC-6.0 timezone."
    yield {"KOSMORRO_TIMEZONE": "America/Chicago"}, [
        "-d2020-07-27"
    ], "Note: All the hours are given in the UTC-5.0 timezone."


@pytest.mark.parametrize(
    "environment, args, expected_stdout_line", timezone_with_deprecated_env_var_input()
)
def test_timezone_with_deprecated_env_var(environment, args, expected_stdout_line):
    result = execute(KOSMORRO + args, environment=environment)
    assert result.successful
    assert (
        "Environment variable KOSMORRO_TIMEZONE is deprecated. Use TZ instead, which is more standard."
        in result.stderr
    )
    assert expected_stdout_line in result.stdout
