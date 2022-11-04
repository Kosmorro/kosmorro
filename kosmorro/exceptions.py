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
from babel.dates import format_date
from kosmorro.i18n.utils import _, SHORT_DATE_FORMAT


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
            minimum_date=format_date(min_date, "long"),
            maximum_date=format_date(max_date, "long"),
        )


class InvalidDateRangeError(RuntimeError):
    def __init__(self, start_date: date, end_date: date):
        super().__init__()
        self.start_date = start_date
        self.end_date = end_date
        self.msg = _(
            "The start date {starting_date} must be before the end date {ending_date}"
        ).format(
            starting_date=format_date(start_date, "long"),
            ending_date=format_date(end_date, "long"),
        )


class InvalidOutputFormatError(RuntimeError):
    def __init__(self, output_format: str, accepted_extensions: [str]):
        super().__init__()
        self.output_format = output_format
        self.accepted_extensions = accepted_extensions
        self.msg = _(
            "Invalid output format: {output_format}. Output file must end with: {accepted_extensions}"
        ).format(
            output_format=output_format,
            accepted_extensions=", ".join(accepted_extensions),
        )


class SearchDatesNotGivenError(RuntimeError):
    def __init__(self):
        super().__init__()
        self.msg = _(
            "Search end date (--until) is required when searching events.'"
        )


class CompileError(RuntimeError):
    def __init__(self, msg):
        super().__init__()
        self.msg = msg
