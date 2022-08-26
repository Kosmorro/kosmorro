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

import requests
from typing import Union

try:
    from importlib.metadata import version
except ImportError:
    from importlib_metadata import version

KOSMORRO_VERSION = version("kosmorro")
KOSMORROLIB_VERSION = version("kosmorrolib")


def get_last_version() -> Union[None, str]:
    try:
        cli = requests.get(
            "https://kosmorro.space/api/SoftwareApplications/cli.json", timeout=0.1
        )
        cli.raise_for_status()
        cli = cli.json()

        return cli["softwareVersion"]
    except requests.RequestException:
        # Could not reach API, assume that the program is up-to-date.
        return None
