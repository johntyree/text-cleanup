#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import division, print_function

import unittest
from parameterized import parameterized

import text_cleanup
import itertools


class TestUtils(unittest.TestCase):
    """Tests for utility functions."""

    def test_flatmap(self):
        result = list(text_cleanup.flatmap(
            lambda i: [i, i+1],
            range(0, 10, 2)))
        expected = list(range(10))
        self.assertEqual(result, expected)

    def test_iterate(self):
        expected = (0, 1, 2, 3, 4)
        result = tuple(text_cleanup.iterate(lambda x: x+1, 0, 4))
        self.assertEqual(result, expected)


class TestMispell(unittest.TestCase):

    @parameterized.expand([
        ('fly', 'fiy'),
        ('liar', 'iiar'),
        ('love', 'iove'),
        ('pillow', 'piiiow'),
        ('Iliad', 'Iiiad'),
    ])
    def testIInsteadOfL(self, expected, given):
        _ok, result = text_cleanup.correct_misspelling(given)
        self.assertEqual(result, expected)

    def testPreserveCapitalLetters(self):
        # Two error solution is Panama....
        expected = 'Ogden'
        _ok, result = text_cleanup.correct_misspelling('Ogten')
        self.assertEqual(result, expected)

    @parameterized.expand([
        ('elephant', 'elephart'),
        ('alphabet', 'lphabet'),
        ('triathlon', 'triathlo'),
    ])
    def testDeletedLetter(self, expected, given):
        _ok, result = text_cleanup.correct_misspelling(given)
        self.assertEqual(result, expected)


class TestMissingSpace(unittest.TestCase):

    @parameterized.expand([
        ('as you', 'asyou'),
    ])
    def test_split(self, expected, given):
        _ok, result = text_cleanup.correct_misspelling(given)
        self.assertEqual(result, expected)



if __name__ == '__main__':
    unittest.main()
