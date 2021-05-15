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

from datetime import date
from _kosmorro.i18n.utils import _, SHORT_DATE_FORMAT


class UnavailableFeatureError(RuntimeError):
    def __init__(self, msg: str):
        super().__init__()
        self.msg = msg


class OutOfRangeDateError(RuntimeError):
    def __init__(self, min_date: date, max_date: date):
        super().__init__()
        self.min_date = min_date
        self.max_date = max_date
        self.msg = _(
            "The date must be between {minimum_date} and {maximum_date}"
        ).format(
            minimum_date=min_date.strftime(SHORT_DATE_FORMAT),
            maximum_date=max_date.strftime(SHORT_DATE_FORMAT),
        )


class CompileError(RuntimeError):
    def __init__(self, msg):
        super().__init__()
        self.msg = msg
