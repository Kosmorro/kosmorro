import unittest

from kosmorrolib import dateutil
from datetime import datetime


class DateUtilTestCase(unittest.TestCase):
    def test_translate_to_timezone(self):
        date = dateutil.translate_to_timezone(datetime(2020, 6, 9, 4), to_tz=-2)
        self.assertEqual(2, date.hour)

        date = dateutil.translate_to_timezone(datetime(2020, 6, 9, 0), to_tz=2)
        self.assertEqual(2, date.hour)

        date = dateutil.translate_to_timezone(datetime(2020, 6, 9, 8), to_tz=2, from_tz=6)
        self.assertEqual(4, date.hour)

        date = dateutil.translate_to_timezone(datetime(2020, 6, 9, 1), to_tz=0, from_tz=2)
        self.assertEqual(8, date.day)
        self.assertEqual(23, date.hour)


if __name__ == '__main__':
    unittest.main()
