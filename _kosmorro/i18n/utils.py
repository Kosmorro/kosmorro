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

import gettext
import os

_LOCALE_DIR = os.path.join(os.path.abspath(os.path.dirname(__file__)), "../locales")
_TRANSLATION = gettext.translation("messages", localedir=_LOCALE_DIR, fallback=True)

_ = _TRANSLATION.gettext

FULL_DATE_FORMAT = _("{day_of_week} {month} {day_number}, {year}").format(
    day_of_week="%A", month="%B", day_number="%d", year="%Y"
)
SHORT_DATETIME_FORMAT = _("{month} {day_number}, {hours}:{minutes}").format(
    month="%b", day_number="%d", hours="%H", minutes="%M"
)
SHORT_DATE_FORMAT = _("{month} {day_number}, {year}").format(
    month="%b", day_number="%d", year="%Y"
)
TIME_FORMAT = _("{hours}:{minutes}").format(hours="%H", minutes="%M")


def ngettext(msgid1, msgid2, number):
    # Not using ngettext = _TRANSLATION.ngettext because the linter will give an invalid-name error otherwise
    return _TRANSLATION.ngettext(msgid1, msgid2, number)
