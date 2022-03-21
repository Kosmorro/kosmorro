#!/usr/bin/env python3

import re
from typing import Union

from kosmorrolib import Position
from openlocationcode import openlocationcode

from .i18n.utils import _


def _parse_latitude_longitude(from_str: str) -> Position:
    if not re.search(r"^([\d.-]+)[,;]([\d.-]+)$", from_str):
        raise ValueError(_("The given position (%s) is not valid." % from_str))

    latitude_longitude = from_str.split(";")
    if len(latitude_longitude) == 1:
        latitude_longitude = from_str.split(",")

    return Position(float(latitude_longitude[0]), float(latitude_longitude[1]))


def _parse_plus_code(from_str: str) -> Union[None, Position]:
    if not openlocationcode.isValid(from_str):
        return None

    if not openlocationcode.isFull(from_str):
        raise ValueError(
            _(
                "The given Plus Code seems to be a short code, please provide a full code."
            )
        )

    pos = openlocationcode.decode(from_str)

    return Position(
        latitude=(pos.latitudeLo + pos.latitudeHi) / 2,
        longitude=(pos.longitudeLo + pos.longitudeHi) / 2,
    )


def get_position(from_str: str) -> Position:
    pos = _parse_plus_code(from_str)

    if pos is not None:
        return pos

    return _parse_latitude_longitude(from_str)
