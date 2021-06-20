#!/usr/bin/env python3

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
