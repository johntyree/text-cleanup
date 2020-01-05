#!/usr/bin/env python
# -*- coding: utf-8 -*-

import unittest
from parameterized import parameterized

from text_cleanup import parse


class TestParser(unittest.TestCase):
    """Tests for the text parser."""

    @parameterized.expand([
        "hello",
        "Hello",
        "HELLO",
        "won't",
        "Can't"])
    def test_is_a_simple_word(self, word):
        self.assertTrue(parse.TOKEN_RE.fullmatch(word))

    @parameterized.expand([
        "tight-lipped",
        "warming-up"])
    def test_is_a_hyphenated_word(self, word):
        self.assertTrue(parse.TOKEN_RE.fullmatch(word))

    @parameterized.expand([
        "hello.",
        "Hello,",
        "HELLO!",
        "won't?",
        '"I',
        'No,"'])
    def test_isnt_a_word(self, word):
        self.assertIsNone(parse.TOKEN_RE.fullmatch(word))


if __name__ == '__main__':
    unittest.main()
