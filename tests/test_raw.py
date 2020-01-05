#!/usr/bin/env python
# -*- coding: utf-8 -*-
# type: ignore
# pylint: disable=missing-docstring
"""Tests for basic cleanup of raw text."""

import unittest
from parameterized import parameterized

from text_cleanup import raw


class TestMispell(unittest.TestCase):

    @parameterized.expand([
        ('fly', 'fiy'),
        ('liar', 'iiar'),
        ('love', 'iove'),
        ('pillow', 'piiiow'),
        ('Iliad', 'Iiiad'),
    ])
    def test_i_instead_of_l(self, expected, given):
        _ok, result = raw.correct_misspelling(given)
        self.assertEqual(result, expected)

    def test_preserve_capital_letters(self):
        expected = 'Yahoo'
        _ok, result = raw.correct_misspelling('Yahoo')
        self.assertEqual(result, expected)

    def test_allow_capitalized(self):
        expected = 'This'
        _ok, result = raw.correct_misspelling('This')
        self.assertEqual(result, expected)

    def test_disallow_lowercased(self):
        expected = 'abraham'
        _ok, result = raw.correct_misspelling('abraham', errors=1)
        self.assertEqual(result, expected)

    @parameterized.expand([
        ('elephant', 'elephart'),
        ('alphabet', 'lphabet'),
        ('triathlon', 'triathlo')])
    def test_deleted_letter(self, expected, given):
        _ok, result = raw.correct_misspelling(given)
        self.assertEqual(result, expected)


class TestMissingSpace(unittest.TestCase):

    @parameterized.expand([
        ('as you', 'asyou'),
        ('I am', 'Iam'),
        ('rapport with', 'rapportwith'),
        ('to understand', 'tounderstand'),
        ('best secretaries', 'bestsecretaries')])
    def test_split(self, expected, given):
        _ok, result = raw.correct_misspelling(given)
        self.assertEqual(result, expected)


class TestEnd2End(unittest.TestCase):
    """Test a full pass over some text, correcting mistakes."""

    def test_noop(self):
        expected = "This text has no errors."
        result = raw.cleanup(expected)
        self.assertEqual(result, expected)

    def test_simple_misspelling(self):
        sample = "This tixt has one error."
        expected = "This text has one error."
        result = raw.cleanup(sample)
        self.assertEqual(result, expected)

    def test_missing_spaces(self):
        sample = "This texthas a few missingspaces."
        expected = "This text has a few missing spaces."
        result = raw.cleanup(sample)
        self.assertEqual(result, expected)

    def test_missing_spaces_with_errors(self):
        sample = "This texthqs missingspaces, but also someerrors."
        expected = "This text has missing spaces, but also some errors."
        result = raw.cleanup(sample)
        self.assertEqual(result, expected)

    def test_complicated_punctuation_noop(self):
        sample = """"Wait! I can't!" he said again-twice that day now."""
        expected = sample
        result = raw.cleanup(expected)
        self.assertEqual(result, expected)

    def test_complicated_punctuation(self):
        sample = """"Wait! I con't!" he said agaon-twice thot day now."""
        expected = """"Wait! I can't!" he said again-twice that day now."""
        result = raw.cleanup(sample)
        self.assertEqual(result, expected)

    def test_complicated_sample(self):
        sample = """
        In the context of 1960, Stranger in a Strange Land was a book that his
        publishers feared-itwas too far off the beaten path. So, in order to
        mini- mize possible losses, Robert was asked to cutthe monuscript down
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
        result = raw.cleanup(sample)
        self.assertEqual(result, expected)

    #  def test_whole_dictionary(self):
        #  """Everything in the dictionary should pass through unscathed."""
        #  # Write this as a giant list comparison for 8x speedup.
        #  expected = list(raw.WORDS)
        #  result = list(map(raw.cleanup, expected))
        #  self.assertEqual(result, expected)

if __name__ == '__main__':
    unittest.main()
