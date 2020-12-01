#!/usr/bin/env python3

#    Kosmorro - Compute The Next Ephemerides
#    Copyright (C) 2019  Jérôme Deuchnord <jerome@deuchnord.fr>
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as
#    published by the Free Software Foundation, either version 3 of the
#    License, or (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU Affero General Public License for more details.
#
#    You should have received a copy of the GNU Affero General Public License
#    along with this program.  If not, see <https://www.gnu.org/licenses/>.

from enum import Enum
from .i18n import _


class MoonPhaseType(Enum):
    NEW_MOON = _('New Moon')
    WAXING_CRESCENT = _('Waxing crescent')
    FIRST_QUARTER = _('First Quarter')
    WAXING_GIBBOUS = _('Waxing gibbous')
    FULL_MOON = _('Full Moon')
    WANING_GIBBOUS = _('Waning gibbous')
    LAST_QUARTER = _('Last Quarter')
    WANING_CRESCENT = _('Waning crescent')


class EventType(Enum):
    OPPOSITION = _('%s is in opposition')
    CONJUNCTION = _('%s and %s are in conjunction')
    OCCULTATION = _('%s occults %s')
    MAXIMAL_ELONGATION = _("%s's largest elongation")
    MOON_PERIGEE = _("%s is at its perigee")
    MOON_APOGEE = _("%s is at its apogee")
