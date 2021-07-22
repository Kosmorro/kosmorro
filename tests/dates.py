import unittest
import kosmorrolib

from datetime import date
from .testutil import run_cmd, IntegrationTestCase
from _kosmorro.i18n import strings


class DateCommandTestCase(IntegrationTestCase):
    def test_invalid_string(self):
        r = run_cmd(self.env, "--date=this-is-a-highly-invalid-string", accept_non_zero=True)
        self.assertEqual(255, r.returncode)
        self.assertEqual(
            r.stdout,
            "\x1b[1m\x1b[31mThe date this-is-a-highly-invalid-string does not match "
            "the required YYYY-MM-DD format or the offset format.\x1b[0m\n"
        )

    def test_invalid_date(self):
        r = run_cmd(self.env, "--date=2020-13-32", accept_non_zero=True)
        self.assertEqual(255, r.returncode)
        self.assertEqual(
            r.stdout,
            "\x1b[1m\x1b[31mThe date 2020-13-32 is not valid: month must be in 1..12\x1b[0m\n"
        )

    def test_specific_date(self):
        asked_date = date(2020, 1, 27)
        expected_moon_phase = kosmorrolib.get_moon_phase(for_date=asked_date)

        for arg in ['--date', '-d']:
            r = run_cmd(self.env, "%s 2020-01-27" % arg)
            self.assertRegex(
                r.stdout,
                r"^%s\n\nMoon phase: %s\n%s on .+\n\n" % (
                    asked_date.strftime("%A %B %d, %Y"),
                    strings.from_moon_phase(expected_moon_phase.phase_type),
                    strings.from_moon_phase(expected_moon_phase.get_next_phase())
                )
            )


if __name__ == '__main__':
    unittest.main()
