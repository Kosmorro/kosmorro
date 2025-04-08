#!/usr/bin/env python3

from .utils import (
    execute,
    KOSMORRO,
)


def test_lunar_eclipse_wording():
    result = execute(KOSMORRO + ["--date=2025-03-14"])
    assert result.successful
    assert "4:07\u202fAM  Total lunar eclipse until 9:50\u202fAM" in result.stdout


def test_seasons():
    result = execute(KOSMORRO + ["--date=2025-03-20"])
    assert result.successful
    assert "9:01\u202fAM  March equinox" in result.stdout

    result = execute(KOSMORRO + ["--date=2025-06-21"])
    assert result.successful
    assert "2:42\u202fAM  June solstice" in result.stdout

    result = execute(KOSMORRO + ["--date=2025-09-22"])
    assert result.successful
    assert "6:19\u202fPM   September equinox" in result.stdout

    result = execute(KOSMORRO + ["--date=2025-12-21"])
    assert result.successful
    assert "3:03\u202fPM  December solstice" in result.stdout
