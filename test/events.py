import unittest

from datetime import date

from kosmorrolib import events
from kosmorrolib.data import Event
from kosmorrolib.core import get_timescale


class MyTestCase(unittest.TestCase):
    def test_event_only_accepts_valid_values(self):
        with self.assertRaises(ValueError):
            Event('SUPERNOVA', None, get_timescale().now())

    def test_find_oppositions(self):
        # Test case: Mars opposition
        # Source of the information: https://promenade.imcce.fr/en/pages6/887.html#mar
        o1 = (events.search_events(date(2020, 10, 13)), '^2020-10-13T23:25')
        o2 = (events.search_events(date(2022, 12, 8)), '^2022-12-08T05:41')
        o3 = (events.search_events(date(2025, 1, 16)), '^2025-01-16T02:38')
        o4 = (events.search_events(date(2027, 2, 19)), '^2027-02-19T15:50')

        for (o, expected_date) in [o1, o2, o3, o4]:
            self.assertEqual(1, len(o), 'Expected 1 event for %s, got %d' % (expected_date, len(o)))
            self.assertEqual('OPPOSITION', o[0].event_type)
            self.assertEqual('MARS', o[0].object.skyfield_name)
            self.assertRegex(o[0].start_time.utc_iso(), expected_date)
            self.assertIsNone(o[0].end_time)
            self.assertEqual('Mars is in opposition', o[0].get_description())


if __name__ == '__main__':
    unittest.main()
