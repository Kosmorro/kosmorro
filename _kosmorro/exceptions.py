#!/usr/bin/env python3

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
