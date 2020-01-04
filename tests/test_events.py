#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import division, print_function

import unittest
from parameterized import parameterized
from nose.plugins.attrib import attr

import text_cleanup
import itertools


class TestUtils(unittest.TestCase):
    """Tests for utility functions."""

    def test_iterate(self):
        expected = (0, 1, 2, 3, 4)
        result = tuple(text_cleanup.iterate(lambda x: x+1, 0, 4))
        self.assertEqual(result, expected)

    @parameterized.expand([
        "hello",
        "Hello",
        "HELLO",
        "won't",
        "Can't"])
    def test_is_a_simple_word(self, word):
        self.assertTrue(text_cleanup.TOKEN_RE.fullmatch(word))

    @parameterized.expand([
        "tight-lipped",
        "warming-up"])
    def test_is_a_hyphenated_word(self, word):
        self.assertTrue(text_cleanup.TOKEN_RE.fullmatch(word))

    @parameterized.expand([
        "hello.",
        "Hello,",
        "HELLO!",
        "won't?",
        '"I',
        'No,"'])
    def test_isnt_a_word(self, word):
        self.assertIsNone(text_cleanup.TOKEN_RE.fullmatch(word))


class TestMispell(unittest.TestCase):

    @parameterized.expand([
        ('fly', 'fiy'),
        ('liar', 'iiar'),
        ('love', 'iove'),
        ('pillow', 'piiiow'),
        ('Iliad', 'Iiiad'),
    ])
    def test_i_instead_of_l(self, expected, given):
        _ok, result = text_cleanup.correct_misspelling(given)
        self.assertEqual(result, expected)

    def test_preserve_capital_letters(self):
        expected = 'Yahoo'
        _ok, result = text_cleanup.correct_misspelling('Yahoo')
        self.assertEqual(result, expected)

    def test_allow_capitalized(self):
        expected = 'This'
        _ok, result = text_cleanup.correct_misspelling('This')
        self.assertEqual(result, expected)

    def test_disallow_lowercased(self):
        expected = 'abraham'
        _ok, result = text_cleanup.correct_misspelling('abraham', errors=1)
        self.assertEqual(result, expected)

    @parameterized.expand([
        ('elephant', 'elephart'),
        ('alphabet', 'lphabet'),
        ('triathlon', 'triathlo')])
    def test_deleted_letter(self, expected, given):
        _ok, result = text_cleanup.correct_misspelling(given)
        self.assertEqual(result, expected)


class TestMissingSpace(unittest.TestCase):

    @parameterized.expand([
        ('as you', 'asyou'),
        ('I am', 'Iam'),
        ('rapport with', 'rapportwith'),
        ('to understand', 'tounderstand'),
        ('best secretaries', 'bestsecretaries')])
    def test_split(self, expected, given):
        _ok, result = text_cleanup.correct_misspelling(given)
        self.assertEqual(result, expected)


class TestEnd2End(unittest.TestCase):
    """Test a full pass over some text, correcting mistakes."""

    def test_noop(self):
        expected = "This text has no errors."
        result = text_cleanup.cleanup(expected)
        self.assertEqual(result, expected)

    def test_simple_misspelling(self):
        sample = "This tixt has one error."
        expected = "This text has one error."
        result = text_cleanup.cleanup(expected)
        self.assertEqual(result, expected)

    def test_missing_spaces(self):
        sample = "This texthas a few missingspaces."
        expected = "This text has a few missing spaces."
        result = text_cleanup.cleanup(expected)
        self.assertEqual(result, expected)

    def test_missing_spaces_with_errors(self):
        sample = "This texthos missingspaces, but also someerrorrs."
        expected = "This text has missing spaces, but also some errors."
        result = text_cleanup.cleanup(expected)
        self.assertEqual(result, expected)

    def test_missing_spaces_with_errors(self):
        sample = "This texthos missingspaces, but also someerrorrs."
        expected = "This text has missing spaces, but also some errors."
        result = text_cleanup.cleanup(expected)
        self.assertEqual(result, expected)

    def test_complicated_punctuation_noop(self):
        sample = """"Wait! I can't!" he said again-twice that day now."""
        expected = sample
        result = text_cleanup.cleanup(expected)
        self.assertEqual(result, expected)

    def test_complicated_punctuation(self):
        sample = """"Wait! I cin't!" he said agrin-twice thot day now."""
        expected = """"Wait! I can't!" he said again-twice that day now."""
        result = text_cleanup.cleanup(expected)
        self.assertEqual(result, expected)

    def test_complicated_sample(self):
        sample = """
        In the context of 1960, Stranger in a Strange Land was a book that his
        publishers feared-itwas too far off the beaten path. So, in order to
        mini- mize possible lisses, Robert was asked to cutthe monuscript down
        to 150,000 words-a loss of about 70,000 words. Other changes were
        alsorequested, before the editor was willing to take a chance on
        publication.
        """
        expected = """
        In the context of 1960, Stranger in a Strange Land was a book that his
        publishers feared-it was too far off the beaten path. So, in order to
        minimize possible losses, Robert was asked to cut the manuscript down
        to 150,000 words-a loss of about 70,000 words. Other changes were
        also requested, before the editor was willing to take a chance on
        publication.
        """
        result = text_cleanup.cleanup(expected)
        self.assertEqual(result, expected)

    def test_whole_dictionary(self):
        """Everything in the dictionary should pass through unscathed."""
        # Write this as a giant list comparison for 8x speedup.
        expected = list(text_cleanup.WORDS)
        result = list(map(text_cleanup.cleanup, expected))
        self.assertEqual(result, expected)

if __name__ == '__main__':
    unittest.main()
