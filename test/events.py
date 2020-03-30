import unittest

from datetime import date, datetime

from kosmorrolib import events
from kosmorrolib.data import Event, ASTERS
from kosmorrolib.core import get_timescale
from unittest_data_provider import data_provider


class EventTestCase(unittest.TestCase):
    def setUp(self) -> None:
        self.maxDiff = None

    def test_event_only_accepts_valid_values(self):
        with self.assertRaises(ValueError):
            Event('SUPERNOVA', None, get_timescale().now())

    expected_events_provider = lambda: (
        (date(2020, 2, 7), []),

        (date(2020, 10, 13), [Event('OPPOSITION', [ASTERS[4]], datetime(2020, 10, 13, 23, 25))]),

        (date(2022, 12, 8), [Event('CONJUNCTION', [ASTERS[1], ASTERS[4]], datetime(2022, 12, 8, 4, 18)),
                             Event('OPPOSITION', [ASTERS[4]], datetime(2022, 12, 8, 5, 41))]),

        (date(2025, 1, 16), [Event('OPPOSITION', [ASTERS[4]], datetime(2025, 1, 16, 2, 38))]),

        (date(2027, 2, 19), [Event('OPPOSITION', [ASTERS[4]], datetime(2027, 2, 19, 15, 50))]),

        (date(2020, 1, 2), [Event('CONJUNCTION', [ASTERS[2], ASTERS[5]], datetime(2020, 1, 2, 16, 41))]),

        (date(2020, 1, 12), [Event('CONJUNCTION', [ASTERS[2], ASTERS[6]], datetime(2020, 1, 12, 9, 51)),
                             Event('CONJUNCTION', [ASTERS[2], ASTERS[9]], datetime(2020, 1, 12, 10, 13)),
                             Event('CONJUNCTION', [ASTERS[6], ASTERS[9]], datetime(2020, 1, 12, 16, 57))]),

        (date(2020, 2, 10), [Event('MAXIMAL_ELONGATION', [ASTERS[2]], datetime(2020, 2, 10, 13, 46), details='18.2°')]),

        (date(2020, 3, 24), [Event('MAXIMAL_ELONGATION', [ASTERS[2]], datetime(2020, 3, 24, 1, 56), details='27.8°'),
                             Event('MAXIMAL_ELONGATION', [ASTERS[3]], datetime(2020, 3, 24, 21, 58), details='46.1°')]),

        (date(2005, 6, 16), [Event('OCCULTATION', [ASTERS[1], ASTERS[5]], datetime(2005, 6, 16, 6, 31))])
    )

    @data_provider(expected_events_provider)
    def test_search_events(self, d: date, expected_events: [Event]):
        actual_events = events.search_events(d)
        self.assertEqual(len(expected_events), len(actual_events),
                         'Expected %d elements, got %d for date %s.' % (len(expected_events),
                                                                        len(actual_events),
                                                                        d.isoformat()))

        for i, expected_event in enumerate(expected_events):
            actual_event = actual_events[i]
            # Remove unnecessary precision (seconds and microseconds)
            actual_event.start_time = datetime(actual_event.start_time.year,
                                               actual_event.start_time.month,
                                               actual_event.start_time.day,
                                               actual_event.start_time.hour,
                                               actual_event.start_time.minute)

            self.assertEqual(expected_event.__dict__, actual_event.__dict__)


if __name__ == '__main__':
    unittest.main()
