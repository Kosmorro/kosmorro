#!/usr/bin/env python3

import unittest

from abc import ABC
from scripttest import TestFileEnvironment, ProcResult

BASE_COMMAND = '../kosmorro --no-colors'


nb_runs = 0


def run_cmd(env: TestFileEnvironment, args: str = "", accept_non_zero: bool = False) -> ProcResult:
    return env.run("%s %s" % (BASE_COMMAND, args), expect_stderr=True, expect_error=accept_non_zero)


class IntegrationTestCase(ABC, unittest.TestCase):
    def setUp(self) -> None:
        self.env = TestFileEnvironment('cli-tests')
        self.env.clear()
        self.env.environ['LANG'] = "C"
        self.env.environ['KOSMORRO_TIMEZONE'] = "0"
