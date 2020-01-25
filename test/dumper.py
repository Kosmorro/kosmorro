import unittest
from datetime import date

from kosmorrolib.data import AsterEphemerides, Planet, MoonPhase, Event
from kosmorrolib.dumper import JsonDumper, TextDumper, _LatexDumper
from kosmorrolib.core import get_timescale


class DumperTestCase(unittest.TestCase):
    def setUp(self) -> None:
        self.maxDiff = None

    def test_json_dumper_returns_correct_json(self):
        data = self._get_data()
        self.assertEqual('{\n'
                         '    "moon_phase": {\n'
                         '        "next_phase_date": "2019-10-21T00:00:00Z",\n'
                         '        "phase": "FULL_MOON",\n'
                         '        "date": "2019-10-14T00:00:00Z"\n'
                         '    },\n'
                         '    "events": [\n'
                         '        {\n'
                         '            "event_type": "OPPOSITION",\n'
                         '            "objects": [\n'
                         '                "Mars"\n'
                         '            ],\n'
                         '            "start_time": "2018-07-27T05:12:00Z",\n'
                         '            "end_time": null\n'
                         '        }\n'
                         '    ],\n'
                         '    "ephemerides": [\n'
                         '        {\n'
                         '            "object": "Mars",\n'
                         '            "details": {\n'
                         '                "rise_time": null,\n'
                         '                "culmination_time": null,\n'
                         '                "set_time": null\n'
                         '            }\n'
                         '        }\n'
                         '    ]\n'
                         '}', JsonDumper(data,
                                         self._get_events()
                                         ).to_string())

    def test_text_dumper_without_events(self):
        ephemerides = self._get_data()
        self.assertEqual('Monday October 14, 2019\n\n'
                         'Object     Rise time    Culmination time    Set time\n'
                         '--------  -----------  ------------------  ----------\n'
                         'Mars           -               -               -\n\n'
                         'Moon phase: Full Moon\n'
                         'Last Quarter on Monday October 21, 2019 at 00:00\n\n'
                         'Note: All the hours are given in UTC.',
                         TextDumper(ephemerides, [], date=date(2019, 10, 14), with_colors=False).to_string())

    def test_text_dumper_with_events(self):
        ephemerides = self._get_data()
        self.assertEqual('Monday October 14, 2019\n\n'
                         'Object     Rise time    Culmination time    Set time\n'
                         '--------  -----------  ------------------  ----------\n'
                         'Mars           -               -               -\n\n'
                         'Moon phase: Full Moon\n'
                         'Last Quarter on Monday October 21, 2019 at 00:00\n\n'
                         'Expected events:\n'
                         '05:12  Mars is in opposition\n\n'
                         'Note: All the hours are given in UTC.',
                         TextDumper(ephemerides, self._get_events(), date=date(2019, 10, 14), with_colors=False).to_string())

    def test_text_dumper_without_ephemerides_and_with_events(self):
        ephemerides = self._get_data(False)
        self.assertEqual('Monday October 14, 2019\n\n'
                         'Moon phase: Full Moon\n'
                         'Last Quarter on Monday October 21, 2019 at 00:00\n\n'
                         'Expected events:\n'
                         '05:12  Mars is in opposition\n\n'
                         'Note: All the hours are given in UTC.',
                         TextDumper(ephemerides, self._get_events(), date=date(2019, 10, 14), with_colors=False).to_string())

    def test_latex_dumper(self):
        latex = _LatexDumper(self._get_data(), self._get_events(), date=date(2019, 10, 14)).to_string()
        self.assertRegex(latex, 'Monday October 14, 2019')
        self.assertRegex(latex, 'Full Moon')
        self.assertRegex(latex, r'\\section{\\sffamily Expected events}')
        self.assertRegex(latex, r'\\section{\\sffamily Ephemerides of the day}')
        self.assertRegex(latex, r'\\object\{Mars\}\{-\}\{-\}\{-\}')
        self.assertRegex(latex, r'\\event\{05:12\}\{Mars is in opposition\}')

        latex = _LatexDumper(self._get_data(aster_rise_set=True),
                             self._get_events(), date=date(2019, 10, 14)).to_string()
        self.assertRegex(latex, r'\\object\{Mars\}\{08:00\}\{13:00\}\{23:00\}')

    def test_latex_dumper_without_ephemerides(self):
        latex = _LatexDumper(self._get_data(False), self._get_events(), date=date(2019, 10, 14)).to_string()
        self.assertRegex(latex, 'Monday October 14, 2019')
        self.assertRegex(latex, 'Full Moon')
        self.assertRegex(latex, r'\\section{\\sffamily Expected events}')
        self.assertRegex(latex, r'\\event\{05:12\}\{Mars is in opposition\}')

        self.assertNotRegex(latex, r'\\object\{Mars\}\{-\}\{-\}\{-\}')
        self.assertNotRegex(latex, r'\\section{\\sffamily Ephemerides of the day}')

    def test_latex_dumper_without_events(self):
        latex = _LatexDumper(self._get_data(), [], date=date(2019, 10, 14)).to_string()
        self.assertRegex(latex, 'Monday October 14, 2019')
        self.assertRegex(latex, 'Full Moon')
        self.assertRegex(latex, r'\\object\{Mars\}\{-\}\{-\}\{-\}')
        self.assertRegex(latex, r'\\section{\\sffamily Ephemerides of the day}')

        self.assertNotRegex(latex, r'\\section{\\sffamily Expected events}')

    @staticmethod
    def _get_data(has_ephemerides: bool = True, aster_rise_set=False):
        rise_time = get_timescale().utc(2019, 10, 14, 8) if aster_rise_set else None
        culmination_time = get_timescale().utc(2019, 10, 14, 13) if aster_rise_set else None
        set_time = get_timescale().utc(2019, 10, 14, 23) if aster_rise_set else None

        return {
            'moon_phase': MoonPhase('FULL_MOON', get_timescale().utc(2019, 10, 14), get_timescale().utc(2019, 10, 21)),
            'details': [Planet('Mars', 'MARS',
                               AsterEphemerides(rise_time, culmination_time, set_time))] if has_ephemerides else []
        }

    @staticmethod
    def _get_events():
        return [Event('OPPOSITION',
                      [Planet('Mars', 'MARS')],
                      get_timescale().utc(2018, 7, 27, 5, 12))
                ]


if __name__ == '__main__':
    unittest.main()
