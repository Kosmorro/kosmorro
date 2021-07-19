#!/usr/bin/env python3

from .utils import _

from kosmorrolib import EventType, MoonPhaseType, ObjectIdentifier, Event


def from_event(event: Event, with_description: bool = True) -> str:
    string, details = {
        EventType.OPPOSITION: (_("%s is in opposition"), None),
        EventType.CONJUNCTION: (_("%s and %s are in conjunction"), None),
        EventType.OCCULTATION: (_("%s occults %s"), None),
        EventType.MAXIMAL_ELONGATION: (
            _("Elongation of %s is maximal"),
            (
                "{:.3n}°".format(event.details["deg"])
                if type(event.details) is dict
                else event.details
            ),
        ),
        EventType.MOON_PERIGEE: (_("%s is at its perigee"), None),
        EventType.MOON_APOGEE: (_("%s is at its apogee"), None),
    }.get(event.event_type)

    if string is None:
        return None

    string = string % tuple([from_object(o.identifier) for o in event.objects])

    if details is not None and with_description:
        return "%s (%s)" % (string, details)

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
        ObjectIdentifier.MARS: _("Mars"),
        ObjectIdentifier.JUPITER: _("Jupiter"),
        ObjectIdentifier.SATURN: _("Saturn"),
        ObjectIdentifier.URANUS: _("Uranus"),
        ObjectIdentifier.NEPTUNE: _("Neptune"),
        ObjectIdentifier.PLUTO: _("Pluto"),
    }.get(identifier)
