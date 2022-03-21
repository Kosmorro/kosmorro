#!/usr/bin/env python3

import re

from dateutil.relativedelta import relativedelta
from datetime import date

from kosmorro.i18n.utils import _


def parse_date(date_arg: str) -> date:
    if re.match(r"^\d{4}-\d{2}-\d{2}$", date_arg):
        try:
            return date.fromisoformat(date_arg)
        except ValueError as error:
            raise ValueError(
                _("The date {date} is not valid: {error}").format(
                    date=date_arg, error=error.args[0]
                )
            ) from error
    elif re.match(r"^([+-])(([0-9]+)y)?[ ]?(([0-9]+)m)?[ ]?(([0-9]+)d)?$", date_arg):

        def get_offset(date_arg: str, signifier: str):
            if re.search(r"([0-9]+)" + signifier, date_arg):
                return abs(
                    int(re.search(r"[+-]?([0-9]+)" + signifier, date_arg).group(0)[:-1])
                )
            return 0

        days = get_offset(date_arg, "d")
        months = get_offset(date_arg, "m")
        years = get_offset(date_arg, "y")

        if date_arg[0] == "+":
            return date.today() + relativedelta(days=days, months=months, years=years)
        return date.today() - relativedelta(days=days, months=months, years=years)

    else:
        error_msg = _(
            "The date {date} does not match the required YYYY-MM-DD format or the offset format."
        )
        raise ValueError(error_msg.format(date=date_arg))
