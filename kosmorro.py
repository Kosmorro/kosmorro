#    Kosmorro - Compute The Next Ephemeris
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
import dumper
from ephemeris import Ephemeris


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
    day = args.date
    position = {'lat': args.latitude, 'lon': args.longitude, 'alt': args.altitude}

    if day is not None and month is None:
        month = date.today().month

    ephemeris = Ephemeris(position)
    ephemerides = ephemeris.compute_ephemeris(year, month, day)

    dump = dumper.TextDumper(ephemerides)
    print(dump.to_string())


def get_args():
    parser = argparse.ArgumentParser(description='Compute the ephemeris for a given day/month/year.',
                                     epilog='By default, the observer will be set at position (0,0) with an altitude'
                                            ' of 0. You will more likely want to change that.')
    parser.add_argument('--latitude', '-lat', type=float, default=0., help="The observer's position on Earth"
                                                                           " (latitude)")
    parser.add_argument('--longitude', '-lon', type=float, default=0., help="The observer's position on Earth"
                                                                            " (longitude)")
    parser.add_argument('--altitude', '-alt', type=float, default=0., help="The observer's position on Earth"
                                                                           " (altitude)")
    parser.add_argument('--date', '-d', type=int, help='A number between 1 and 28, 29, 30 or 31 (depending on the'
                                                       ' month). The date you want to compute the ephemeris for')
    parser.add_argument('--month', '-m', type=int, help='A number between 1 and 12. The month you want to compute the'
                                                        ' ephemeris for (defaults to the current month if the day is'
                                                        ' defined)')
    parser.add_argument('year', type=int, help='The year you want to compute the ephemeris for')

    return parser.parse_args()


if __name__ == '__main__':
    main()
