import unittest

import kosmorrolib.core as core


class CoreTestCase(unittest.TestCase):
    def test_flatten_list(self):
        self.assertEqual([0, 1, 2, 3, 4, 5, 6, 7, 8, 9], core.flatten_list([0, 1, 2, [3, 4, [5, 6], 7], 8, [9]]))


if __name__ == '__main__':
    unittest.main()
