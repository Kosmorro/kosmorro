import argparse
import numpy
from datetime import date
from ephemeris import Ephemeris
import json


# Fixes the "TypeError: Object of type int64 is not JSON serializable"
# See https://stackoverflow.com/a/50577730
def json_default(o):
    if isinstance(o, numpy.int64):
        return int(o)
    raise TypeError('Object of type ' + str(type(o)) + ' could not be integrated in the JSON')


def main():
    args = get_args()
    year = args.year
    month = args.month
    day = args.date
    position = {'lat': args.latitude, 'lon': args.longitude, 'altitude': args.altitude}

    if day is not None and month is None:
        month = date.today().month

    ephemeris = Ephemeris(position)
    e = ephemeris.compute_ephemeris(year, month, day)

    print(json.dumps(e, default=json_default, indent=4, separators=(',', ': ')))


def get_args():
    parser = argparse.ArgumentParser(description='Compute the ephemeris for a given day/month/year, by default for'
                                                 ' Paris, France.', epilog='By default, the observer will be set at'
                                                                           ' position (0,0) with an altitude of 0.'
                                                                           ' You will more likely want to change that.')
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


if '__main__' == __name__:
    main()
