import unittest

import os
import kosmorrolib.core as core


class CoreTestCase(unittest.TestCase):
    def test_flatten_list(self):
        self.assertEqual([0, 1, 2, 3, 4, 5, 6, 7, 8, 9], core.flatten_list([0, 1, 2, [3, 4, [5, 6], 7], 8, [9]]))

    def test_get_env(self):
        self.assertEqual(0, len(core.get_env()))

        os.environ['SOME_RANDOM_VAR'] = 'an awesome value'
        self.assertEqual(0, len(core.get_env()))

        os.environ['KOSMORRO_GREAT_VARIABLE'] = 'value'
        env = core.get_env()
        self.assertEqual(1, len(env))
        self.assertEqual('value', env.great_variable)

        os.environ['KOSMORRO_ANOTHER_VARIABLE'] = 'another value'
        env = core.get_env()
        self.assertEqual(2, len(env))
        self.assertEqual('value', env.great_variable)
        self.assertEqual('another value', env.another_variable)

        self.assertEqual("{'great_variable': 'value', 'another_variable': 'another value'}", str(env))


if __name__ == '__main__':
    unittest.main()
