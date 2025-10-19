#!/usr/bin/env python3

from typing import Union
from babel.dates import format_time
from .utils import _
from kosmorrolib import (
    EventType,
    MoonPhaseType,
    ObjectIdentifier,
    Event,
    SeasonType,
    LunarEclipseType,
)


def from_event(event: Event) -> Union[None, str]:
    string = None
    match event.event_type:
        case EventType.OPPOSITION:
            string, details = (
                _("%s is in opposition") % from_object(event.objects[0].identifier),
                None,
            )
        case EventType.CONJUNCTION:
            string, details = (
                _("%s and %s are in conjunction")
                % (
                    from_object(event.objects[0].identifier),
                    from_object(event.objects[1].identifier),
                ),
                None,
            )
        case EventType.OCCULTATION:
            string, details = (
                _("%s occults %s")
                % (
                    from_object(event.objects[0].identifier),
                    from_object(event.objects[1].identifier),
                ),
                None,
            )
        case EventType.MAXIMAL_ELONGATION:
            string, details = (
                _("Elongation of %s is maximal")
                % from_object(event.objects[0].identifier),
                lambda e: "{:.3n}°".format(e.details["deg"]),
            )
        case EventType.PERIGEE:
            string, details = (
                _("%s is at its periapsis") % from_object(event.objects[0].identifier),
                None,
            )
        case EventType.APOGEE:
            string, details = (
                _("%s is at its apoapsis") % from_object(event.objects[0].identifier),
                None,
            )
        case EventType.SEASON_CHANGE:
            match event.details["season"]:
                case SeasonType.MARCH_EQUINOX:
                    string = _("March equinox")
                case SeasonType.JUNE_SOLSTICE:
                    string = _("June solstice")
                case SeasonType.SEPTEMBER_EQUINOX:
                    string = _("September equinox")
                case _:
                    string = _("December solstice")

            details = None
        case EventType.LUNAR_ECLIPSE:
            match event.details["type"]:
                case LunarEclipseType.TOTAL:
                    string = _("Total lunar eclipse until %(hour)s") % {
                        "hour": format_time(event.end_time, "short")
                    }

                case LunarEclipseType.PENUMBRAL:
                    string = _("Penumbral lunar eclipse until %(hour)s") % {
                        "hour": format_time(event.end_time, "short")
                    }

                case LunarEclipseType.PARTIAL:
                    string = _("Partial lunar eclipse until %(hour)s") % {
                        "hour": format_time(event.end_time, "short")
                    }

            details = None
        case _:
            return None

    if details is not None:
        return "%s (%s)" % (string, details(event))

    return string


def from_moon_phase(moon_phase: MoonPhaseType) -> str:
    string = {
        MoonPhaseType.NEW_MOON: _("New Moon"),
        MoonPhaseType.WAXING_CRESCENT: _("Waxing Crescent"),
        MoonPhaseType.FIRST_QUARTER: _("First Quarter"),
        MoonPhaseType.WAXING_GIBBOUS: _("Waxing Gibbous"),
        MoonPhaseType.FULL_MOON: _("Full Moon"),
        MoonPhaseType.WANING_GIBBOUS: _("Waning Gibbous"),
        MoonPhaseType.LAST_QUARTER: _("Last Quarter"),
        MoonPhaseType.WANING_CRESCENT: _("Waning Crescent"),
    }.get(moon_phase)

    if string is None:
        raise RuntimeError("Unknown moon phase: %s." % moon_phase)

    return string


def from_object(identifier: ObjectIdentifier) -> str:
    return {
        ObjectIdentifier.SUN: _("Sun"),
        ObjectIdentifier.MOON: _("Moon"),
        ObjectIdentifier.MERCURY: _("Mercury"),
        ObjectIdentifier.VENUS: _("Venus"),
        ObjectIdentifier.EARTH: _("Earth"),
        ObjectIdentifier.MARS: _("Mars"),
        ObjectIdentifier.JUPITER: _("Jupiter"),
        ObjectIdentifier.SATURN: _("Saturn"),
        ObjectIdentifier.URANUS: _("Uranus"),
        ObjectIdentifier.NEPTUNE: _("Neptune"),
        ObjectIdentifier.PLUTO: _("Pluto"),
    }.get(identifier)
