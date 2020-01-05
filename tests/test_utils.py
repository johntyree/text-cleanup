#!/usr/bin/env python
# -*- coding: utf-8 -*-

import unittest

from text_cleanup import utils


class TestUtils(unittest.TestCase):
    """Tests for utility functions."""

    def test_iterate(self):
        expected = (0, 1, 2, 3, 4)
        result = tuple(utils.iterate(lambda x: x+1, 0, 4))
        self.assertEqual(result, expected)


if __name__ == '__main__':
    unittest.main()
