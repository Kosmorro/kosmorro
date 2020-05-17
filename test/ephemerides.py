import unittest
from .testutils import expect_assertions
from kosmorrolib import ephemerides
from kosmorrolib.data import EARTH, Position, MoonPhase
from datetime import date


class EphemeridesTestCase(unittest.TestCase):
    def test_get_ephemerides_for_aster_returns_correct_hours(self):
        position = Position(0, 0, EARTH)
        eph = ephemerides.get_ephemerides(date=date(2019, 11, 18),
                                          position=position)

        @expect_assertions(self.assertRegex, num=3)
        def do_assertions(assert_regex):
            for ephemeris in eph:
                if ephemeris.object.skyfield_name == 'SUN':
                    assert_regex(ephemeris.rise_time.isoformat(), '^2019-11-18T05:41:')
                    assert_regex(ephemeris.culmination_time.isoformat(), '^2019-11-18T11:45:')
                    assert_regex(ephemeris.set_time.isoformat(), '^2019-11-18T17:48:')
                    break

        do_assertions()

    ###################################################################################################################
    ###                                             MOON PHASE TESTS                                                ###
    ###################################################################################################################

    def test_moon_phase_new_moon(self):
        phase = ephemerides.get_moon_phase(date(2019, 11, 25))
        self.assertEqual('WANING_CRESCENT', phase.identifier)
        self.assertIsNone(phase.time)
        self.assertRegexpMatches(phase.next_phase_date.isoformat(), '^2019-11-26T')

        phase = ephemerides.get_moon_phase(date(2019, 11, 26))
        self.assertEqual('NEW_MOON', phase.identifier)
        self.assertRegexpMatches(phase.next_phase_date.isoformat(), '^2019-12-04T')

        phase = ephemerides.get_moon_phase(date(2019, 11, 27))
        self.assertEqual('WAXING_CRESCENT', phase.identifier)
        self.assertIsNone(phase.time)
        self.assertRegexpMatches(phase.next_phase_date.isoformat(), '^2019-12-04T')

    def test_moon_phase_first_crescent(self):
        phase = ephemerides.get_moon_phase(date(2019, 11, 3))
        self.assertEqual('WAXING_CRESCENT', phase.identifier)
        self.assertIsNone(phase.time)
        self.assertRegexpMatches(phase.next_phase_date.isoformat(), '^2019-11-04T')

        phase = ephemerides.get_moon_phase(date(2019, 11, 4))
        self.assertEqual('FIRST_QUARTER', phase.identifier)
        self.assertRegexpMatches(phase.next_phase_date.isoformat(), '^2019-11-12T')

        phase = ephemerides.get_moon_phase(date(2019, 11, 5))
        self.assertEqual('WAXING_GIBBOUS', phase.identifier)
        self.assertIsNone(phase.time)
        self.assertRegexpMatches(phase.next_phase_date.isoformat(), '^2019-11-12T')

    def test_moon_phase_full_moon(self):
        phase = ephemerides.get_moon_phase(date(2019, 11, 11))
        self.assertEqual('WAXING_GIBBOUS', phase.identifier)
        self.assertIsNone(phase.time)
        self.assertRegexpMatches(phase.next_phase_date.isoformat(), '^2019-11-12T')

        phase = ephemerides.get_moon_phase(date(2019, 11, 12))
        self.assertEqual('FULL_MOON', phase.identifier)
        self.assertRegexpMatches(phase.next_phase_date.isoformat(), '^2019-11-19T')

        phase = ephemerides.get_moon_phase(date(2019, 11, 13))
        self.assertEqual('WANING_GIBBOUS', phase.identifier)
        self.assertIsNone(phase.time)
        self.assertRegexpMatches(phase.next_phase_date.isoformat(), '^2019-11-19T')

    def test_moon_phase_last_quarter(self):
        phase = ephemerides.get_moon_phase(date(2019, 11, 18))
        self.assertEqual('WANING_GIBBOUS', phase.identifier)
        self.assertIsNone(phase.time)
        self.assertRegexpMatches(phase.next_phase_date.isoformat(), '^2019-11-19T')

        phase = ephemerides.get_moon_phase(date(2019, 11, 19))
        self.assertEqual('LAST_QUARTER', phase.identifier)
        self.assertRegexpMatches(phase.next_phase_date.isoformat(), '^2019-11-26T')

        phase = ephemerides.get_moon_phase(date(2019, 11, 20))
        self.assertEqual('WANING_CRESCENT', phase.identifier)
        self.assertIsNone(phase.time)
        self.assertRegexpMatches(phase.next_phase_date.isoformat(), '^2019-11-26T')

    def test_moon_phase_prediction(self):
        phase = MoonPhase('NEW_MOON', None, None)
        self.assertEqual('First Quarter', phase.get_next_phase_name())
        phase = MoonPhase('WAXING_CRESCENT', None, None)
        self.assertEqual('First Quarter', phase.get_next_phase_name())

        phase = MoonPhase('FIRST_QUARTER', None, None)
        self.assertEqual('Full Moon', phase.get_next_phase_name())
        phase = MoonPhase('WAXING_GIBBOUS', None, None)
        self.assertEqual('Full Moon', phase.get_next_phase_name())

        phase = MoonPhase('FULL_MOON', None, None)
        self.assertEqual('Last Quarter', phase.get_next_phase_name())
        phase = MoonPhase('WANING_GIBBOUS', None, None)
        self.assertEqual('Last Quarter', phase.get_next_phase_name())

        phase = MoonPhase('LAST_QUARTER', None, None)
        self.assertEqual('New Moon', phase.get_next_phase_name())
        phase = MoonPhase('WANING_CRESCENT', None, None)
        self.assertEqual('New Moon', phase.get_next_phase_name())


if __name__ == '__main__':
    unittest.main()
