#!/usr/bin/env python3

import re

from kosmorrolib import Position

from .i18n.utils import _


def get_position(from_str: str) -> Position:
    if not re.search(r"^([\d.-]+)[,;]([\d.-]+)$", from_str):
        raise ValueError(_("The given position (%s) is not valid." % from_str))

    latitude_longitude = from_str.split(";")
    if len(latitude_longitude) == 1:
        latitude_longitude = from_str.split(",")

    return Position(float(latitude_longitude[0]), float(latitude_longitude[1]))
