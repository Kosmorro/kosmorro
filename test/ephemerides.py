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


if __name__ == '__main__':
    unittest.main()
