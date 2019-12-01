import unittest
from kosmorrolib.ephemerides import EphemeridesComputer
from kosmorrolib.core import get_skf_objects
from kosmorrolib.data import Star, Position
from datetime import date


class EphemeridesComputerTestCase(unittest.TestCase):
    def test_get_ephemerides_for_aster_returns_correct_hours(self):
        position = Position(0, 0)
        position.observation_planet = get_skf_objects()['earth']
        star = EphemeridesComputer.get_asters_ephemerides_for_aster(Star('Sun', skyfield_name='sun'),
                                                                    date=date(2019, 11, 18),
                                                                    position=position)

        self.assertEqual('2019-11-18T05:41:31Z', star.ephemerides.rise_time.utc_iso())
        self.assertEqual('2019-11-18T11:45:02Z', star.ephemerides.culmination_time.utc_iso())
        self.assertEqual('2019-11-18T17:48:39Z', star.ephemerides.set_time.utc_iso())

    ###################################################################################################################
    ###                                             MOON PHASE TESTS                                                ###
    ###################################################################################################################

    def test_moon_phase_new_moon(self):
        phase = EphemeridesComputer.get_moon_phase(2019, 11, 25)
        self.assertEqual('WANING_CRESCENT', phase.identifier)
        self.assertIsNone(phase.time)
        self.assertRegexpMatches(phase.next_phase_date.utc_iso(), '^2019-11-26T')

        phase = EphemeridesComputer.get_moon_phase(2019, 11, 26)
        self.assertEqual('NEW_MOON', phase.identifier)
        self.assertRegexpMatches(phase.next_phase_date.utc_iso(), '^2019-12-04T')

        phase = EphemeridesComputer.get_moon_phase(2019, 11, 27)
        self.assertEqual('WAXING_CRESCENT', phase.identifier)
        self.assertIsNone(phase.time)
        self.assertRegexpMatches(phase.next_phase_date.utc_iso(), '^2019-12-04T')

    def test_moon_phase_first_crescent(self):
        phase = EphemeridesComputer.get_moon_phase(2019, 11, 3)
        self.assertEqual('WAXING_CRESCENT', phase.identifier)
        self.assertIsNone(phase.time)
        self.assertRegexpMatches(phase.next_phase_date.utc_iso(), '^2019-11-04T')

        phase = EphemeridesComputer.get_moon_phase(2019, 11, 4)
        self.assertEqual('FIRST_QUARTER', phase.identifier)
        self.assertRegexpMatches(phase.next_phase_date.utc_iso(), '^2019-11-12T')

        phase = EphemeridesComputer.get_moon_phase(2019, 11, 5)
        self.assertEqual('WAXING_GIBBOUS', phase.identifier)
        self.assertIsNone(phase.time)
        self.assertRegexpMatches(phase.next_phase_date.utc_iso(), '^2019-11-12T')

    def test_moon_phase_full_moon(self):
        phase = EphemeridesComputer.get_moon_phase(2019, 11, 11)
        self.assertEqual('WAXING_GIBBOUS', phase.identifier)
        self.assertIsNone(phase.time)
        self.assertRegexpMatches(phase.next_phase_date.utc_iso(), '^2019-11-12T')

        phase = EphemeridesComputer.get_moon_phase(2019, 11, 12)
        self.assertEqual('FULL_MOON', phase.identifier)
        self.assertRegexpMatches(phase.next_phase_date.utc_iso(), '^2019-11-19T')

        phase = EphemeridesComputer.get_moon_phase(2019, 11, 13)
        self.assertEqual('WANING_GIBBOUS', phase.identifier)
        self.assertIsNone(phase.time)
        self.assertRegexpMatches(phase.next_phase_date.utc_iso(), '^2019-11-19T')

    def test_moon_phase_last_quarter(self):
        phase = EphemeridesComputer.get_moon_phase(2019, 11, 18)
        self.assertEqual('WANING_GIBBOUS', phase.identifier)
        self.assertIsNone(phase.time)
        self.assertRegexpMatches(phase.next_phase_date.utc_iso(), '^2019-11-19T')

        phase = EphemeridesComputer.get_moon_phase(2019, 11, 19)
        self.assertEqual('LAST_QUARTER', phase.identifier)
        self.assertRegexpMatches(phase.next_phase_date.utc_iso(), '^2019-11-26T')

        phase = EphemeridesComputer.get_moon_phase(2019, 11, 20)
        self.assertEqual('WANING_CRESCENT', phase.identifier)
        self.assertIsNone(phase.time)
        self.assertRegexpMatches(phase.next_phase_date.utc_iso(), '^2019-11-26T')


if __name__ == '__main__':
    unittest.main()
