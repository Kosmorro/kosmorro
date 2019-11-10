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

import argparse
from datetime import date
import numpy
from kosmorrolib import dumper
from kosmorrolib.ephemerides import EphemeridesComputer, Position


# Fixes the "TypeError: Object of type int64 is not JSON serializable"
# See https://stackoverflow.com/a/50577730
def json_default(obj):
    if isinstance(obj, numpy.int64):
        return int(obj)
    raise TypeError('Object of type ' + str(type(obj)) + ' could not be integrated in the JSON')


def main():
    args = get_args()
    year = args.year
    month = args.month
    day = args.day

    if day is not None and month is None:
        month = date.today().month

    ephemeris = EphemeridesComputer(Position(args.latitude, args.longitude, altitude=args.altitude))
    ephemerides = ephemeris.compute_ephemerides(year, month, day)

    dump = dumper.TextDumper(ephemerides)
    print(dump.to_string())


def get_args():
    today = date.today()

    parser = argparse.ArgumentParser(description='Compute the ephemerides for a given date, at a given position'
                                                 ' on Earth.',
                                     epilog='By default, the ephemerides will be computed for today (%s) for an'
                                            ' observer positioned at coordinates (0,0), with an altitude of 0.'
                                     % today.strftime('%a %b %d, %Y'))

    parser.add_argument('--latitude', '-lat', type=float, default=0.,
                        help="The observer's latitude on Earth")
    parser.add_argument('--longitude', '-lon', type=float, default=0.,
                        help="The observer's longitude on Earth")
    parser.add_argument('--altitude', '-alt', type=float, default=0.,
                        help="The observer's altitude on Earth")
    parser.add_argument('--day', '-d', type=int, default=today.day,
                        help='A number between 1 and 28, 29, 30 or 31 (depending on the month). The day you want to '
                             ' compute the ephemerides for. Defaults to %d (the current day).' % today.day)
    parser.add_argument('--month', '-m', type=int, default=today.month,
                        help='A number between 1 and 12. The month you want to compute the ephemerides for. Defaults to'
                             ' %d (the current month).' % today.month)
    parser.add_argument('--year', '-y', type=int, default=today.year,
                        help='The year you want to compute the ephemerides for.'
                             ' Defaults to %d (the current year).' % today.year)

    return parser.parse_args()


if __name__ == '__main__':
    main()
