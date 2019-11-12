import unittest
from kosmorrolib.data import AsterEphemerides, Planet
from kosmorrolib.dumper import JsonDumper


class DumperTestCase(unittest.TestCase):
    def test_json_dumper_returns_correct_json(self):
        data = self._get_data()
        self.assertEqual('{\n'
                         '    "moon_phase": "FULL_MOON",\n'
                         '    "details": [\n'
                         '        {\n'
                         '            "name": "Mars",\n'
                         '            "ephemerides": {\n'
                         '                "rise_time": null,\n'
                         '                "culmination_time": null,\n'
                         '                "set_time": null\n'
                         '            }\n'
                         '        }\n'
                         '    ]\n'
                         '}', JsonDumper(data).to_string())

    @staticmethod
    def _get_data():
        return {
            'moon_phase': 'FULL_MOON',
            'details': [Planet('Mars', 'MARS', AsterEphemerides(None, None, None))]
        }


if __name__ == '__main__':
    unittest.main()
