import unittest
from datetime import date, datetime

from kosmorrolib.data import AsterEphemerides, Planet, MoonPhase, Event
from kosmorrolib.dumper import JsonDumper, TextDumper, _LatexDumper


class DumperTestCase(unittest.TestCase):
    def setUp(self) -> None:
        self.maxDiff = None

    def test_json_dumper_returns_correct_json(self):
        self.assertEqual('{\n'
                         '    "ephemerides": [\n'
                         '        {\n'
                         '            "object": {\n'
                         '                "name": "Mars",\n'
                         '                "type": "planet",\n'
                         '                "radius": null\n'
                         '            },\n'
                         '            "rise_time": null,\n'
                         '            "culmination_time": null,\n'
                         '            "set_time": null\n'
                         '        }\n'
                         '    ],\n'
                         '    "moon_phase": {\n'
                         '        "phase": "FULL_MOON",\n'
                         '        "time": "2019-10-14T00:00:00",\n'
                         '        "next": {\n'
                         '            "phase": "LAST_QUARTER",\n'
                         '            "time": "2019-10-21T00:00:00"\n'
                         '        }\n'
                         '    },\n'
                         '    "events": [\n'
                         '        {\n'
                         '            "objects": [\n'
                         '                {\n'
                         '                    "name": "Mars",\n'
                         '                    "type": "planet",\n'
                         '                    "radius": null\n'
                         '                }\n'
                         '            ],\n'
                         '            "event": "OPPOSITION",\n'
                         '            "starts_at": "2019-10-14T23:00:00",\n'
                         '            "ends_at": null,\n'
                         '            "details": null\n'
                         '        },\n'
                         '        {\n'
                         '            "objects": [\n'
                         '                {\n'
                         '                    "name": "Venus",\n'
                         '                    "type": "planet",\n'
                         '                    "radius": null\n'
                         '                }\n'
                         '            ],\n'
                         '            "event": "MAXIMAL_ELONGATION",\n'
                         '            "starts_at": "2019-10-14T12:00:00",\n'
                         '            "ends_at": null,\n'
                         '            "details": "42.0\\u00b0"\n'
                         '        }\n'
                         '    ]\n'
                         '}', JsonDumper(self._get_ephemerides(), self._get_moon_phase(), self._get_events()).to_string())

        self.assertEqual('{\n'
                         '    "ephemerides": [\n'
                         '        {\n'
                         '            "object": {\n'
                         '                "name": "Mars",\n'
                         '                "type": "planet",\n'
                         '                "radius": null\n'
                         '            },\n'
                         '            "rise_time": "2019-10-14T08:00:00",\n'
                         '            "culmination_time": "2019-10-14T13:00:00",\n'
                         '            "set_time": "2019-10-14T23:00:00"\n'
                         '        }\n'
                         '    ],\n'
                         '    "moon_phase": {\n'
                         '        "phase": "FULL_MOON",\n'
                         '        "time": "2019-10-14T00:00:00",\n'
                         '        "next": {\n'
                         '            "phase": "LAST_QUARTER",\n'
                         '            "time": "2019-10-21T00:00:00"\n'
                         '        }\n'
                         '    },\n'
                         '    "events": [\n'
                         '        {\n'
                         '            "objects": [\n'
                         '                {\n'
                         '                    "name": "Mars",\n'
                         '                    "type": "planet",\n'
                         '                    "radius": null\n'
                         '                }\n'
                         '            ],\n'
                         '            "event": "OPPOSITION",\n'
                         '            "starts_at": "2019-10-14T23:00:00",\n'
                         '            "ends_at": null,\n'
                         '            "details": null\n'
                         '        },\n'
                         '        {\n'
                         '            "objects": [\n'
                         '                {\n'
                         '                    "name": "Venus",\n'
                         '                    "type": "planet",\n'
                         '                    "radius": null\n'
                         '                }\n'
                         '            ],\n'
                         '            "event": "MAXIMAL_ELONGATION",\n'
                         '            "starts_at": "2019-10-14T12:00:00",\n'
                         '            "ends_at": null,\n'
                         '            "details": "42.0\\u00b0"\n'
                         '        }\n'
                         '    ]\n'
                         '}', JsonDumper(self._get_ephemerides(aster_rise_set=True), self._get_moon_phase(),
                                         self._get_events()).to_string())

    def test_text_dumper_without_events(self):
        ephemerides = self._get_ephemerides()
        self.assertEqual('Monday October 14, 2019\n\n'
                         'Object     Rise time    Culmination time    Set time\n'
                         '--------  -----------  ------------------  ----------\n'
                         'Mars           -               -               -\n\n'
                         'Moon phase: Full Moon\n'
                         'Last Quarter on Monday October 21, 2019 at 00:00\n\n'
                         'Note: All the hours are given in UTC.',
                         TextDumper(ephemerides, self._get_moon_phase(), [], date=date(2019, 10, 14), with_colors=False).to_string())

        ephemerides = self._get_ephemerides(aster_rise_set=True)
        self.assertEqual('Monday October 14, 2019\n\n'
                         'Object     Rise time    Culmination time    Set time\n'
                         '--------  -----------  ------------------  ----------\n'
                         'Mars         08:00           13:00           23:00\n\n'
                         'Moon phase: Full Moon\n'
                         'Last Quarter on Monday October 21, 2019 at 00:00\n\n'
                         'Note: All the hours are given in UTC.',
                         TextDumper(ephemerides, self._get_moon_phase(), [], date=date(2019, 10, 14), with_colors=False).to_string())

    def test_text_dumper_with_events(self):
        ephemerides = self._get_ephemerides()
        self.assertEqual("Monday October 14, 2019\n\n"
                         "Object     Rise time    Culmination time    Set time\n"
                         "--------  -----------  ------------------  ----------\n"
                         "Mars           -               -               -\n\n"
                         "Moon phase: Full Moon\n"
                         "Last Quarter on Monday October 21, 2019 at 00:00\n\n"
                         "Expected events:\n"
                         "23:00  Mars is in opposition\n"
                         "12:00  Venus's largest elongation (42.0°)\n\n"
                         "Note: All the hours are given in UTC.",
                         TextDumper(ephemerides, self._get_moon_phase(), self._get_events(), date=date(2019, 10, 14), with_colors=False).to_string())

    def test_text_dumper_without_ephemerides_and_with_events(self):
        self.assertEqual('Monday October 14, 2019\n\n'
                         'Moon phase: Full Moon\n'
                         'Last Quarter on Monday October 21, 2019 at 00:00\n\n'
                         'Expected events:\n'
                         '23:00  Mars is in opposition\n'
                         "12:00  Venus's largest elongation (42.0°)\n\n"
                         'Note: All the hours are given in UTC.',
                         TextDumper(None, self._get_moon_phase(), self._get_events(),
                                    date=date(2019, 10, 14), with_colors=False).to_string())

    def test_timezone_is_taken_in_account(self):
        ephemerides = self._get_ephemerides(aster_rise_set=True)

        self.assertEqual('Monday October 14, 2019\n\n'
                         'Object     Rise time    Culmination time     Set time\n'
                         '--------  -----------  ------------------  -------------\n'
                         'Mars         09:00           14:00         Oct 15, 00:00\n\n'
                         'Moon phase: Full Moon\n'
                         'Last Quarter on Monday October 21, 2019 at 01:00\n\n'
                         'Expected events:\n'
                         'Oct 15, 00:00  Mars is in opposition\n'
                         "13:00          Venus's largest elongation (42.0°)\n\n"
                         'Note: All the hours are given in the UTC+1 timezone.',
                         TextDumper(ephemerides, self._get_moon_phase(), self._get_events(), date=date(2019, 10, 14),
                                    with_colors=False, timezone=1).to_string())

        ephemerides = self._get_ephemerides(aster_rise_set=True)

        self.assertEqual('Monday October 14, 2019\n\n'
                         'Object     Rise time    Culmination time    Set time\n'
                         '--------  -----------  ------------------  ----------\n'
                         'Mars         07:00           12:00           22:00\n\n'
                         'Moon phase: Full Moon\n'
                         'Last Quarter on Sunday October 20, 2019 at 23:00\n\n'
                         'Expected events:\n'
                         '22:00  Mars is in opposition\n'
                         "11:00  Venus's largest elongation (42.0°)\n\n"
                         'Note: All the hours are given in the UTC-1 timezone.',
                         TextDumper(ephemerides, self._get_moon_phase(), self._get_events(), date=date(2019, 10, 14),
                                    with_colors=False, timezone=-1).to_string())

    def test_latex_dumper(self):
        latex = _LatexDumper(self._get_ephemerides(), self._get_moon_phase(), self._get_events(),
                             date=date(2019, 10, 14)).to_string()

        self.assertRegex(latex, 'Monday October 14, 2019')
        self.assertRegex(latex, 'Full Moon')
        self.assertRegex(latex, r'\\section{\\sffamily Expected events}')
        self.assertRegex(latex, r'\\section{\\sffamily Ephemerides of the day}')
        self.assertRegex(latex, r'\\object\{Mars\}\{-\}\{-\}\{-\}')
        self.assertRegex(latex, r'\\event\{23:00\}\{Mars is in opposition\}')
        self.assertRegex(latex, r"\\event\{12:00\}\{Venus's largest elongation \(42.0°\)\}")

        latex = _LatexDumper(self._get_ephemerides(aster_rise_set=True), self._get_moon_phase(),
                             self._get_events(), date=date(2019, 10, 14)).to_string()
        self.assertRegex(latex, r'\\object\{Mars\}\{08:00\}\{13:00\}\{23:00\}')

    def test_latex_dumper_without_ephemerides(self):
        latex = _LatexDumper(None, self._get_moon_phase(), self._get_events(),
                             date=date(2019, 10, 14)).to_string()

        self.assertRegex(latex, 'Monday October 14, 2019')
        self.assertRegex(latex, 'Full Moon')
        self.assertRegex(latex, r'\\section{\\sffamily Expected events}')
        self.assertRegex(latex, r'\\event\{23:00\}\{Mars is in opposition\}')
        self.assertRegex(latex, r"\\event\{12:00\}\{Venus's largest elongation \(42.0°\)\}")

        self.assertNotRegex(latex, r'\\object\{Mars\}\{-\}\{-\}\{-\}')
        self.assertNotRegex(latex, r'\\section{\\sffamily Ephemerides of the day}')

    def test_latex_dumper_without_events(self):
        latex = _LatexDumper(self._get_ephemerides(), self._get_moon_phase(), [], date=date(2019, 10, 14)).to_string()

        self.assertRegex(latex, 'Monday October 14, 2019')
        self.assertRegex(latex, 'Full Moon')
        self.assertRegex(latex, r'\\object\{Mars\}\{-\}\{-\}\{-\}')
        self.assertRegex(latex, r'\\section{\\sffamily Ephemerides of the day}')

        self.assertNotRegex(latex, r'\\section{\\sffamily Expected events}')

    def test_latex_dumper_with_graph(self):
        latex = _LatexDumper(self._get_ephemerides(True), self._get_moon_phase(), self._get_events(),
                             date=date(2019, 10, 14), show_graph=True).to_string()

        self.assertRegex(latex, 'Monday October 14, 2019')
        self.assertRegex(latex, 'Full Moon')
        self.assertRegex(latex, r'\\section{\\sffamily Expected events}')
        self.assertRegex(latex, r'\\section{\\sffamily Ephemerides of the day}')
        self.assertRegex(latex, r'\\graphobject\{18\}\{gray\}\{8\}\{0\}\{23\}\{0\}\{08:00\}\{23:00\}')
        self.assertRegex(latex, r'\\event\{23:00\}\{Mars is in opposition\}')
        self.assertRegex(latex, r"\\event\{12:00\}\{Venus's largest elongation \(42.0°\)\}")

        latex = _LatexDumper(self._get_ephemerides(aster_rise_set=True), self._get_moon_phase(),
                             self._get_events(), date=date(2019, 10, 14)).to_string()
        self.assertRegex(latex, r'\\object\{Mars\}\{08:00\}\{13:00\}\{23:00\}')

    def test_latex_dumper_with_graph_but_without_rise_time(self):
        ephemerides = self._get_ephemerides(True)
        ephemerides[0].rise_time = None
        latex = _LatexDumper(ephemerides, self._get_moon_phase(), self._get_events(),
                             date=date(2019, 10, 14), show_graph=True).to_string()

        self.assertRegex(latex, 'Monday October 14, 2019')
        self.assertRegex(latex, 'Full Moon')
        self.assertRegex(latex, r'\\section{\\sffamily Expected events}')
        self.assertRegex(latex, r'\\section{\\sffamily Ephemerides of the day}')
        self.assertRegex(latex, r'\\graphobject\{18\}\{gray\}\{0\}\{0\}\{23\}\{0\}\{\}\{23:00\}')
        self.assertRegex(latex, r'\\event\{23:00\}\{Mars is in opposition\}')
        self.assertRegex(latex, r"\\event\{12:00\}\{Venus's largest elongation \(42.0°\)\}")

        latex = _LatexDumper(self._get_ephemerides(aster_rise_set=True), self._get_moon_phase(),
                             self._get_events(), date=date(2019, 10, 14)).to_string()
        self.assertRegex(latex, r'\\object\{Mars\}\{08:00\}\{13:00\}\{23:00\}')

    def test_latex_dumper_with_graph_but_without_set_time(self):
        ephemerides = self._get_ephemerides(True)
        ephemerides[0].set_time = None
        latex = _LatexDumper(ephemerides, self._get_moon_phase(), self._get_events(),
                             date=date(2019, 10, 14), show_graph=True).to_string()

        self.assertRegex(latex, 'Monday October 14, 2019')
        self.assertRegex(latex, 'Full Moon')
        self.assertRegex(latex, r'\\section{\\sffamily Expected events}')
        self.assertRegex(latex, r'\\section{\\sffamily Ephemerides of the day}')
        self.assertRegex(latex, r'\\graphobject\{18\}\{gray\}\{8\}\{0\}\{24\}\{0\}\{08:00\}\{\}')
        self.assertRegex(latex, r'\\event\{23:00\}\{Mars is in opposition\}')
        self.assertRegex(latex, r"\\event\{12:00\}\{Venus's largest elongation \(42.0°\)\}")

        latex = _LatexDumper(self._get_ephemerides(aster_rise_set=True), self._get_moon_phase(),
                             self._get_events(), date=date(2019, 10, 14)).to_string()
        self.assertRegex(latex, r'\\object\{Mars\}\{08:00\}\{13:00\}\{23:00\}')

    def test_latex_dumper_with_graph_but_mars_sets_tomorrow(self):
        ephemerides = self._get_ephemerides(True)
        ephemerides[0].set_time = datetime(2019, 10, 15, 1)
        latex = _LatexDumper(ephemerides, self._get_moon_phase(), self._get_events(),
                             date=date(2019, 10, 14), show_graph=True).to_string()

        self.assertRegex(latex, 'Monday October 14, 2019')
        self.assertRegex(latex, 'Full Moon')
        self.assertRegex(latex, r'\\section{\\sffamily Expected events}')
        self.assertRegex(latex, r'\\section{\\sffamily Ephemerides of the day}')
        self.assertRegex(latex, r'\\graphobject\{18\}\{gray\}\{8\}\{0\}\{24\}\{0\}\{08:00\}\{\}')
        self.assertRegex(latex, r'\\graphobject\{18\}\{gray\}\{0\}\{0\}\{1\}\{0\}\{\}\{Oct 15, 01:00\}')
        self.assertRegex(latex, r'\\event\{23:00\}\{Mars is in opposition\}')
        self.assertRegex(latex, r"\\event\{12:00\}\{Venus's largest elongation \(42.0°\)\}")

        latex = _LatexDumper(self._get_ephemerides(aster_rise_set=True), self._get_moon_phase(),
                             self._get_events(), date=date(2019, 10, 14)).to_string()
        self.assertRegex(latex, r'\\object\{Mars\}\{08:00\}\{13:00\}\{23:00\}')

    @staticmethod
    def _get_ephemerides(aster_rise_set=False) -> [AsterEphemerides]:
        rise_time = datetime(2019, 10, 14, 8) if aster_rise_set else None
        culmination_time = datetime(2019, 10, 14, 13) if aster_rise_set else None
        set_time = datetime(2019, 10, 14, 23) if aster_rise_set else None

        return [AsterEphemerides(rise_time, culmination_time, set_time, Planet('Mars', 'MARS'))]

    @staticmethod
    def _get_moon_phase():
        return MoonPhase('FULL_MOON', datetime(2019, 10, 14), datetime(2019, 10, 21))

    @staticmethod
    def _get_events():
        return [Event('OPPOSITION',
                      [Planet('Mars', 'MARS')],
                      datetime(2019, 10, 14, 23, 00)),
                Event('MAXIMAL_ELONGATION',
                      [Planet('Venus', 'VENUS')],
                      datetime(2019, 10, 14, 12, 00), details='42.0°'),
                ]


if __name__ == '__main__':
    unittest.main()
