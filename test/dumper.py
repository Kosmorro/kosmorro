import unittest
from datetime import date, datetime

from kosmorrolib.data import AsterEphemerides, Planet, MoonPhase, Event
from kosmorrolib.dumper import JsonDumper, TextDumper, _LatexDumper


class DumperTestCase(unittest.TestCase):
    def setUp(self) -> None:
        self.maxDiff = None

    def test_json_dumper_returns_correct_json(self):
        self.assertEqual('{\n'
                         '    "moon_phase": {\n'
                         '        "next_phase_date": "2019-10-21T00:00:00",\n'
                         '        "phase": "FULL_MOON",\n'
                         '        "date": "2019-10-14T00:00:00"\n'
                         '    },\n'
                         '    "events": [\n'
                         '        {\n'
                         '            "event_type": "OPPOSITION",\n'
                         '            "objects": [\n'
                         '                "Mars"\n'
                         '            ],\n'
                         '            "start_time": "2019-10-14T23:00:00",\n'
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
                         '}', JsonDumper(self._get_data(), self._get_events()).to_string())

        data = self._get_data(aster_rise_set=True)
        self.assertEqual('{\n'
                         '    "moon_phase": {\n'
                         '        "next_phase_date": "2019-10-21T00:00:00",\n'
                         '        "phase": "FULL_MOON",\n'
                         '        "date": "2019-10-14T00:00:00"\n'
                         '    },\n'
                         '    "events": [\n'
                         '        {\n'
                         '            "event_type": "OPPOSITION",\n'
                         '            "objects": [\n'
                         '                "Mars"\n'
                         '            ],\n'
                         '            "start_time": "2019-10-14T23:00:00",\n'
                         '            "end_time": null\n'
                         '        }\n'
                         '    ],\n'
                         '    "ephemerides": [\n'
                         '        {\n'
                         '            "object": "Mars",\n'
                         '            "details": {\n'
                         '                "rise_time": "2019-10-14T08:00:00",\n'
                         '                "culmination_time": "2019-10-14T13:00:00",\n'
                         '                "set_time": "2019-10-14T23:00:00"\n'
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

        ephemerides = self._get_data(aster_rise_set=True)
        self.assertEqual('Monday October 14, 2019\n\n'
                         'Object     Rise time    Culmination time    Set time\n'
                         '--------  -----------  ------------------  ----------\n'
                         'Mars         08:00           13:00           23:00\n\n'
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
                         '23:00  Mars is in opposition\n\n'
                         'Note: All the hours are given in UTC.',
                         TextDumper(ephemerides, self._get_events(), date=date(2019, 10, 14), with_colors=False).to_string())

    def test_text_dumper_without_ephemerides_and_with_events(self):
        ephemerides = self._get_data(False)
        self.assertEqual('Monday October 14, 2019\n\n'
                         'Moon phase: Full Moon\n'
                         'Last Quarter on Monday October 21, 2019 at 00:00\n\n'
                         'Expected events:\n'
                         '23:00  Mars is in opposition\n\n'
                         'Note: All the hours are given in UTC.',
                         TextDumper(ephemerides, self._get_events(), date=date(2019, 10, 14), with_colors=False).to_string())

    def test_timezone_is_taken_in_account(self):
        ephemerides = self._get_data(aster_rise_set=True)
        self.assertEqual('Monday October 14, 2019\n\n'
                         'Object     Rise time    Culmination time     Set time\n'
                         '--------  -----------  ------------------  -------------\n'
                         'Mars         09:00           14:00         Oct 15, 00:00\n\n'
                         'Moon phase: Full Moon\n'
                         'Last Quarter on Monday October 21, 2019 at 01:00\n\n'
                         'Expected events:\n'
                         'Oct 15, 00:00  Mars is in opposition\n\n'
                         'Note: All the hours are given in the UTC+1 timezone.',
                         TextDumper(ephemerides, self._get_events(), date=date(2019, 10, 14), with_colors=False, timezone=1).to_string())

        ephemerides = self._get_data(aster_rise_set=True)
        self.assertEqual('Monday October 14, 2019\n\n'
                         'Object     Rise time    Culmination time    Set time\n'
                         '--------  -----------  ------------------  ----------\n'
                         'Mars         07:00           12:00           22:00\n\n'
                         'Moon phase: Full Moon\n'
                         'Last Quarter on Sunday October 20, 2019 at 23:00\n\n'
                         'Expected events:\n'
                         '22:00  Mars is in opposition\n\n'
                         'Note: All the hours are given in the UTC-1 timezone.',
                         TextDumper(ephemerides, self._get_events(), date=date(2019, 10, 14), with_colors=False, timezone=-1).to_string())

    def test_latex_dumper(self):
        latex = _LatexDumper(self._get_data(), self._get_events(), date=date(2019, 10, 14)).to_string()
        self.assertRegex(latex, 'Monday October 14, 2019')
        self.assertRegex(latex, 'Full Moon')
        self.assertRegex(latex, r'\\section{\\sffamily Expected events}')
        self.assertRegex(latex, r'\\section{\\sffamily Ephemerides of the day}')
        self.assertRegex(latex, r'\\object\{Mars\}\{-\}\{-\}\{-\}')
        self.assertRegex(latex, r'\\event\{23:00\}\{Mars is in opposition\}')

        latex = _LatexDumper(self._get_data(aster_rise_set=True),
                             self._get_events(), date=date(2019, 10, 14)).to_string()
        self.assertRegex(latex, r'\\object\{Mars\}\{08:00\}\{13:00\}\{23:00\}')

    def test_latex_dumper_without_ephemerides(self):
        latex = _LatexDumper(self._get_data(False), self._get_events(), date=date(2019, 10, 14)).to_string()
        self.assertRegex(latex, 'Monday October 14, 2019')
        self.assertRegex(latex, 'Full Moon')
        self.assertRegex(latex, r'\\section{\\sffamily Expected events}')
        self.assertRegex(latex, r'\\event\{23:00\}\{Mars is in opposition\}')

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
        rise_time = datetime(2019, 10, 14, 8) if aster_rise_set else None
        culmination_time = datetime(2019, 10, 14, 13) if aster_rise_set else None
        set_time = datetime(2019, 10, 14, 23) if aster_rise_set else None

        return {
            'moon_phase': MoonPhase('FULL_MOON', datetime(2019, 10, 14), datetime(2019, 10, 21)),
            'details': [Planet('Mars', 'MARS',
                               AsterEphemerides(rise_time, culmination_time, set_time))] if has_ephemerides else []
        }

    @staticmethod
    def _get_events():
        return [Event('OPPOSITION',
                      [Planet('Mars', 'MARS')],
                      datetime(2019, 10, 14, 23, 00))
                ]


if __name__ == '__main__':
    unittest.main()
