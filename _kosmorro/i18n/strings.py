#!/usr/bin/env python3

from .utils import _

from kosmorrolib import EventType, MoonPhaseType, ObjectIdentifier, Event


def from_event(event: Event) -> str:
    return {
        EventType.OPPOSITION: _("%s is in opposition"),
        EventType.CONJUNCTION: _("%s and %s are in conjunction"),
        EventType.OCCULTATION: _("%s occults %s"),
        EventType.MAXIMAL_ELONGATION: _("Elongation of %s is maximal"),
        EventType.MOON_PERIGEE: _("%s is at its perigee"),
        EventType.MOON_APOGEE: _("%s is at its apogee"),
    }.get(event.event_type) % tuple([from_object(o.identifier) for o in event.objects])


def from_moon_phase(moon_phase: MoonPhaseType) -> str:
    return {
        MoonPhaseType.NEW_MOON: _("New Moon"),
        MoonPhaseType.WAXING_CRESCENT: _("Waxing Crescent"),
        MoonPhaseType.FIRST_QUARTER: _("First Quarter"),
        MoonPhaseType.WAXING_GIBBOUS: _("Waxing Gibbous"),
        MoonPhaseType.FULL_MOON: _("Full Moon"),
        MoonPhaseType.WANING_GIBBOUS: _("Waning Gibbous"),
        MoonPhaseType.LAST_QUARTER: _("Last Quarter"),
        MoonPhaseType.WANING_CRESCENT: _("Waning Crescent"),
    }.get(moon_phase, _("Unknown phase"))


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
    }.get(identifier, _("Unknown object"))
