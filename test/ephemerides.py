import unittest

from .testutils import expect_assertions
from kosmorrolib import ephemerides
from kosmorrolib.data import EARTH, Position, MoonPhase
from kosmorrolib.enum import MoonPhaseType

from datetime import date
from kosmorrolib.exceptions import OutOfRangeDateError


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
        self.assertEqual(MoonPhaseType.WANING_CRESCENT, phase.phase_type)
        self.assertIsNone(phase.time)
        self.assertRegexpMatches(phase.next_phase_date.isoformat(), '^2019-11-26T')

        phase = ephemerides.get_moon_phase(date(2019, 11, 26))
        self.assertEqual(MoonPhaseType.NEW_MOON, phase.phase_type)
        self.assertRegexpMatches(phase.next_phase_date.isoformat(), '^2019-12-04T')

        phase = ephemerides.get_moon_phase(date(2019, 11, 27))
        self.assertEqual(MoonPhaseType.WAXING_CRESCENT, phase.phase_type)
        self.assertIsNone(phase.time)
        self.assertRegexpMatches(phase.next_phase_date.isoformat(), '^2019-12-04T')

    def test_moon_phase_first_crescent(self):
        phase = ephemerides.get_moon_phase(date(2019, 11, 3))
        self.assertEqual(MoonPhaseType.WAXING_CRESCENT, phase.phase_type)
        self.assertIsNone(phase.time)
        self.assertRegexpMatches(phase.next_phase_date.isoformat(), '^2019-11-04T')

        phase = ephemerides.get_moon_phase(date(2019, 11, 4))
        self.assertEqual(MoonPhaseType.FIRST_QUARTER, phase.phase_type)
        self.assertRegexpMatches(phase.next_phase_date.isoformat(), '^2019-11-12T')

        phase = ephemerides.get_moon_phase(date(2019, 11, 5))
        self.assertEqual(MoonPhaseType.WAXING_GIBBOUS, phase.phase_type)
        self.assertIsNone(phase.time)
        self.assertRegexpMatches(phase.next_phase_date.isoformat(), '^2019-11-12T')

    def test_moon_phase_full_moon(self):
        phase = ephemerides.get_moon_phase(date(2019, 11, 11))
        self.assertEqual(MoonPhaseType.WAXING_GIBBOUS, phase.phase_type)
        self.assertIsNone(phase.time)
        self.assertRegexpMatches(phase.next_phase_date.isoformat(), '^2019-11-12T')

        phase = ephemerides.get_moon_phase(date(2019, 11, 12))
        self.assertEqual(MoonPhaseType.FULL_MOON, phase.phase_type)
        self.assertRegexpMatches(phase.next_phase_date.isoformat(), '^2019-11-19T')

        phase = ephemerides.get_moon_phase(date(2019, 11, 13))
        self.assertEqual(MoonPhaseType.WANING_GIBBOUS, phase.phase_type)
        self.assertIsNone(phase.time)
        self.assertRegexpMatches(phase.next_phase_date.isoformat(), '^2019-11-19T')

    def test_moon_phase_last_quarter(self):
        phase = ephemerides.get_moon_phase(date(2019, 11, 18))
        self.assertEqual(MoonPhaseType.WANING_GIBBOUS, phase.phase_type)
        self.assertIsNone(phase.time)
        self.assertRegexpMatches(phase.next_phase_date.isoformat(), '^2019-11-19T')

        phase = ephemerides.get_moon_phase(date(2019, 11, 19))
        self.assertEqual(MoonPhaseType.LAST_QUARTER, phase.phase_type)
        self.assertRegexpMatches(phase.next_phase_date.isoformat(), '^2019-11-26T')

        phase = ephemerides.get_moon_phase(date(2019, 11, 20))
        self.assertEqual(MoonPhaseType.WANING_CRESCENT, phase.phase_type)
        self.assertIsNone(phase.time)
        self.assertRegexpMatches(phase.next_phase_date.isoformat(), '^2019-11-26T')

    def test_moon_phase_prediction(self):
        phase = MoonPhase(MoonPhaseType.NEW_MOON, None, None)
        self.assertEqual(MoonPhaseType.FIRST_QUARTER, phase.get_next_phase())
        phase = MoonPhase(MoonPhaseType.WAXING_CRESCENT, None, None)
        self.assertEqual(MoonPhaseType.FIRST_QUARTER, phase.get_next_phase())

        phase = MoonPhase(MoonPhaseType.FIRST_QUARTER, None, None)
        self.assertEqual(MoonPhaseType.FULL_MOON, phase.get_next_phase())
        phase = MoonPhase(MoonPhaseType.WAXING_GIBBOUS, None, None)
        self.assertEqual(MoonPhaseType.FULL_MOON, phase.get_next_phase())

        phase = MoonPhase(MoonPhaseType.FULL_MOON, None, None)
        self.assertEqual(MoonPhaseType.LAST_QUARTER, phase.get_next_phase())
        phase = MoonPhase(MoonPhaseType.WANING_GIBBOUS, None, None)
        self.assertEqual(MoonPhaseType.LAST_QUARTER, phase.get_next_phase())

        phase = MoonPhase(MoonPhaseType.LAST_QUARTER, None, None)
        self.assertEqual(MoonPhaseType.NEW_MOON, phase.get_next_phase())
        phase = MoonPhase(MoonPhaseType.WANING_CRESCENT, None, None)
        self.assertEqual(MoonPhaseType.NEW_MOON, phase.get_next_phase())

    def test_get_ephemerides_raises_exception_on_out_of_date_range(self):
        with self.assertRaises(OutOfRangeDateError):
            ephemerides.get_ephemerides(date(1789, 5, 5), Position(0, 0, EARTH))

    def test_get_moon_phase_raises_exception_on_out_of_date_range(self):
        with self.assertRaises(OutOfRangeDateError):
            ephemerides.get_moon_phase(date(1789, 5, 5))


if __name__ == '__main__':
    unittest.main()
