import unittest

from kosmorrolib import data, core


class DataTestCase(unittest.TestCase):
    def test_object_radius_must_be_set_to_get_apparent_radius(self):
        o = data.Planet('Saturn', 'SATURN')

        with self.assertRaises(ValueError) as context:
            o.get_apparent_radius(core.get_timescale().now(), core.get_skf_objects()['earth'])

        self.assertEqual(('Missing radius for Saturn object',), context.exception.args)


if __name__ == '__main__':
    unittest.main()
