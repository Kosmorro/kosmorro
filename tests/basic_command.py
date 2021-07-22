import unittest
import kosmorrolib
from _kosmorro.i18n import strings

from datetime import date
from .testutil import run_cmd, IntegrationTestCase


class BasicCommandTestCase(IntegrationTestCase):
    def test_help(self):
        for arg in ['--help', '-h']:
            r = run_cmd(self.env, arg)
            self.assertEqual(0, r.returncode)
            self.assertTrue(
                r.stdout.startswith("usage: kosmorro [-h] [--version] [--clear-cache] [--format {text,json,pdf}]")
            )

    def test_command_without_arguments(self):
        expected_moon_phase = kosmorrolib.get_moon_phase()
        r = run_cmd(self.env)

        self.assertEqual(0, r.returncode)
        self.assertRegex(
            r.stdout,
            r"^%s\n\nMoon phase: %s\n%s on .+\n\n" % (
                date.today().strftime("%A %B %d, %Y"),
                strings.from_moon_phase(expected_moon_phase.phase_type),
                strings.from_moon_phase(expected_moon_phase.get_next_phase())
            )
        )


if __name__ == '__main__':
    unittest.main()
