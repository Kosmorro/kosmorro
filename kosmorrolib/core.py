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

import os
import re
from shutil import rmtree
from pathlib import Path

from datetime import date
from dateutil.relativedelta import relativedelta

from skyfield.api import Loader
from skyfield.timelib import Time
from skyfield.nutationlib import iau2000b

from kosmorrolib.i18n import _

CACHE_FOLDER = str(Path.home()) + '/.kosmorro-cache'

class Environment:
    def __init__(self):
        self._vars = {}

    def __set__(self, key, value):
        self._vars[key] = value

    def __getattr__(self, key):
        return self._vars[key] if key in self._vars else None

    def __str__(self):
        return self._vars.__str__()

    def __len__(self):
        return len(self._vars)

def get_env() -> Environment:
    environment = Environment()

    for var in os.environ:
        if not re.search('^KOSMORRO_', var):
            continue

        [_, env] = var.split('_', 1)
        environment.__set__(env.lower(), os.getenv(var))

    return environment

def get_loader():
    return Loader(CACHE_FOLDER)


def get_timescale():
    return get_loader().timescale()


def get_skf_objects():
    return get_loader()('de421.bsp')


def get_iau2000b(time: Time):
    return iau2000b(time.tt)


def clear_cache():
    rmtree(CACHE_FOLDER)


def flatten_list(the_list: list):
    new_list = []
    for item in the_list:
        if isinstance(item, list):
            for item2 in flatten_list(item):
                new_list.append(item2)
            continue

        new_list.append(item)

    return new_list


def get_date(date_arg: str) -> date:
    if re.match(r'^\d{4}-\d{2}-\d{2}$', date_arg):
        try:
            return date.fromisoformat(date_arg)
        except ValueError as error:
            raise ValueError(_('The date {date} is not valid: {error}').format(date=date_arg, error=error.args[0]))
    elif re.match(r'^([+-])(([0-9]+)y)?[ ]?(([0-9]+)m)?[ ]?(([0-9]+)d)?$', date_arg):
        def get_offset(date_arg: str, signifier: str):
            if re.search(r'([0-9]+)' + signifier, date_arg):
                return abs(int(re.search(r'[+-]?([0-9]+)' + signifier, date_arg).group(0)[:-1]))
            return 0

        days = get_offset(date_arg, 'd')
        months = get_offset(date_arg, 'm')
        years = get_offset(date_arg, 'y')


        if date_arg[0] == '+':
            return date.today() + relativedelta(days=days, months=months, years=years)
        return date.today() - relativedelta(days=days, months=months, years=years)

    else:
        error_msg = _('The date {date} does not match the required YYYY-MM-DD format or the offset format.')
        raise ValueError(error_msg.format(date=date_arg))
