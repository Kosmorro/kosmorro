import unittest
from kosmorrolib.data import AsterEphemerides, Planet, MoonPhase
from kosmorrolib.dumper import JsonDumper
from kosmorrolib.core import get_timescale


class DumperTestCase(unittest.TestCase):
    def test_json_dumper_returns_correct_json(self):
        data = self._get_data()
        self.assertEqual('{\n'
                         '    "moon_phase": {\n'
                         '        "next_phase_date": "2019-11-20T00:00:00Z",\n'
                         '        "phase": "FULL_MOON",\n'
                         '        "date": "2019-11-11T00:00:00Z"\n'
                         '    },\n'
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
            'moon_phase': MoonPhase('FULL_MOON', get_timescale().utc(2019, 11, 11), get_timescale().utc(2019, 11, 20)),
            'details': [Planet('Mars', 'MARS', AsterEphemerides(None, None, None))]
        }


if __name__ == '__main__':
    unittest.main()
