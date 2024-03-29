#!/usr/bin/env python3

from .utils import (
    execute,
    KOSMORRO,
)
import tempfile
from os import path, environ
from sys import platform


def test_json_output():
    result = execute(
        KOSMORRO
        + ["--latitude=50.5876", "--longitude=3.0624", "-d2020-01-27", "--format=json"]
    )
    assert result.is_successful()
    assert (
        result.stdout
        == """{
    "ephemerides": [
        {
            "object": {
                "identifier": "SUN",
                "type": "STAR",
                "radius": 696342
            },
            "rise_time": "2020-01-27T07:31:00",
            "culmination_time": "2020-01-27T12:01:00",
            "set_time": "2020-01-27T16:30:00"
        },
        {
            "object": {
                "identifier": "MOON",
                "type": "SATELLITE",
                "radius": 1737.4
            },
            "rise_time": "2020-01-27T09:06:00",
            "culmination_time": "2020-01-27T14:09:00",
            "set_time": "2020-01-27T19:13:00"
        },
        {
            "object": {
                "identifier": "MERCURY",
                "type": "PLANET",
                "radius": 2439.7
            },
            "rise_time": "2020-01-27T08:10:00",
            "culmination_time": "2020-01-27T12:49:00",
            "set_time": "2020-01-27T17:28:00"
        },
        {
            "object": {
                "identifier": "VENUS",
                "type": "PLANET",
                "radius": 6051.8
            },
            "rise_time": "2020-01-27T09:01:00",
            "culmination_time": "2020-01-27T14:35:00",
            "set_time": "2020-01-27T20:10:00"
        },
        {
            "object": {
                "identifier": "MARS",
                "type": "PLANET",
                "radius": 3396.2
            },
            "rise_time": "2020-01-27T04:19:00",
            "culmination_time": "2020-01-27T08:23:00",
            "set_time": "2020-01-27T12:28:00"
        },
        {
            "object": {
                "identifier": "JUPITER",
                "type": "PLANET",
                "radius": 71492
            },
            "rise_time": "2020-01-27T06:15:00",
            "culmination_time": "2020-01-27T10:18:00",
            "set_time": "2020-01-27T14:21:00"
        },
        {
            "object": {
                "identifier": "SATURN",
                "type": "PLANET",
                "radius": 60268
            },
            "rise_time": "2020-01-27T06:56:00",
            "culmination_time": "2020-01-27T11:09:00",
            "set_time": "2020-01-27T15:22:00"
        },
        {
            "object": {
                "identifier": "URANUS",
                "type": "PLANET",
                "radius": 25559
            },
            "rise_time": "2020-01-27T10:21:00",
            "culmination_time": "2020-01-27T17:25:00",
            "set_time": "2020-01-27T00:33:00"
        },
        {
            "object": {
                "identifier": "NEPTUNE",
                "type": "PLANET",
                "radius": 24764
            },
            "rise_time": "2020-01-27T09:01:00",
            "culmination_time": "2020-01-27T14:36:00",
            "set_time": "2020-01-27T20:10:00"
        },
        {
            "object": {
                "identifier": "PLUTO",
                "type": "PLANET",
                "radius": 1185
            },
            "rise_time": "2020-01-27T06:57:00",
            "culmination_time": "2020-01-27T11:04:00",
            "set_time": "2020-01-27T15:11:00"
        }
    ],
    "moon_phase": {
        "phase": "NEW_MOON",
        "time": "2020-01-24T21:41:59.705921+00:00",
        "next": {
            "phase": "FIRST_QUARTER",
            "time": "2020-02-02T01:41:40.282275+00:00"
        }
    },
    "events": [
        {
            "objects": [
                {
                    "identifier": "VENUS",
                    "type": "PLANET",
                    "radius": 6051.8
                },
                {
                    "identifier": "NEPTUNE",
                    "type": "PLANET",
                    "radius": 24764
                }
            ],
            "EventType": "CONJUNCTION",
            "starts_at": "2020-01-27T20:00:23.242750+00:00",
            "ends_at": null,
            "details": null
        }
    ]
}
"""
    )
