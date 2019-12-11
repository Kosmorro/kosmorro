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
            self.assertEqual('MARS', o[0].objects[0].skyfield_name)
            self.assertRegex(o[0].start_time.utc_iso(), expected_date)
            self.assertIsNone(o[0].end_time)
            self.assertEqual('Mars is in opposition', o[0].get_description())

    def test_find_conjunctions(self):
        # Test case: Mars opposition
        # Source of the information: https://promenade.imcce.fr/en/pages6/887.html#mar
        c1 = (events.search_events(date(2020, 1, 2)), [(['MERCURY', 'JUPITER BARYCENTER'], '^2020-01-02T15:20')])
        c2 = (events.search_events(date(2020, 1, 12)), [(['MERCURY', 'SATURN BARYCENTER'], '^2020-01-12T04:34'),
                                                        (['MERCURY', 'PLUTO BARYCENTER'], '^2020-01-12T06:56')])

        for (c, expected_dates) in [c1, c2]:
            self.assertEqual(len(expected_dates), len(c),
                             'Expected %d event(s) for %s, got %d' % (len(expected_dates), expected_dates, len(c)))

            i = 0
            for conjunction in c:
                self.assertEqual('CONJUNCTION', conjunction.event_type)
                objects, expected_date = expected_dates[i]

                j = 0
                self.assertRegex(conjunction.start_time.utc_iso(), expected_date)
                for object in objects:
                    self.assertEqual(object, conjunction.objects[j].skyfield_name)
                    j += 1

                self.assertIsNone(conjunction.end_time)
                self.assertRegex(conjunction.get_description(), ' are in conjunction$')

                i += 1


if __name__ == '__main__':
    unittest.main()
