#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Functions for cleaning up text, typically from bad OCR scans."""

import functools
import itertools
import string

from typing import Tuple, List, Dict, Set, Iterable, Iterator, Callable, TypeVar

from text_cleanup import parse
from text_cleanup import utils

A = TypeVar('A')  # pylint: disable=invalid-name
B = TypeVar('B')  # pylint: disable=invalid-name

# These are common substitution errors and we should prefer to stay within the
# group when making corrections.
ERROR_GROUPS = (
    'jli!1t',
    'aceo',
    '3B',
    'hmn',
    'yug',
    'MNH',
    'BERPD',
    'QO0',
)
def build_index(groups: Iterable[str]) -> Dict[str, str]:
    """Return dict from elem to group, given iter of groups of elems."""
    tmp: Dict[str, List[str]] = {}
    for group in groups:
        for letter in group:
            tmp.setdefault(letter, []).append(group)
    return {k: ''.join(v) for k, v in tmp.items()}
PREFERRED_ERRORS = build_index(ERROR_GROUPS)


def get_valid_words(filename=None) -> Set[str]:
    """Return set of valid words, read from filename if present."""
    with open(filename or '/usr/share/dict/words') as fin:
        words = fin.read().splitlines()
    # Remove one-letter words that aren't 'a', 'A' or 'I'.
    valid = set(w for w in words if len(w) > 1 or w in 'aAI')
    # Allow any word to be capitalized, since it might start a sentence.
    valid.update(w.capitalize() for w in words if w[0].islower())
    return valid
WORDS = get_valid_words()


def spellcheck(wordstr: str) -> bool:
    """Return true if wordstr is made of valid words, else False."""
    quick = (
        not wordstr or
        wordstr.endswith('-') or
        parse.NUMBER_RE.fullmatch(wordstr) or
        wordstr in WORDS)
    if quick:
        return True

    hyphenated = wordstr.replace('-', ' ').split()
    return hyphenated[0] != wordstr and all(map(spellcheck, hyphenated))


def one_space(word: str) -> Iterable[str]:
    """Yield words made by inserting a single space into word."""
    for i in range(1, len(word)):
        yield word[:i] + ' ' + word[i:]


def one_deletion(word: str) -> Iterable[str]:
    """Yield words made by deleting a single letter from word."""
    for i, letter in enumerate(word):
        yield word[:i] + word[i+1:]


def one_insertion(word: str) -> Iterable[str]:
    """Yield words made by inserting a single letter into word."""
    alphabet = string.ascii_lowercase
    # Add letter before current letter
    for i in range(len(word)):
        for newchar in alphabet:
            yield word[:i] + newchar + word[i:]

    # Add letter at end
    for newchar in alphabet:
        yield word + newchar


def one_substitution(word: str) -> Iterable[str]:
    """Yield words made by substituting a single letter in word."""
    # Check for any preferred errors before trying brute force substitution
    for i, letter in enumerate(word):
        for newchar in PREFERRED_ERRORS.get(letter, ''):
            if newchar != letter:
                yield word[:i] + newchar + word[i+1:]

    # No luck... time to brute force
    alphabet = string.ascii_lowercase
    for i, letter in enumerate(word):
        # Change letter by trying entire alphabet
        for newchar in alphabet:
            if newchar != letter:
                yield word[:i] + newchar + word[i+1:]



def one_error(word: str,
              space: bool = True,
              substitution: bool = True,
              insertion: bool = True,
              deletion: bool = True) -> Iterable[str]:
    """Yield one-error variations on word."""

    # Rewrapping text can leave unnecesarry hyphenations like 'mini-mize'
    unhyphenated = word.replace('-', '')
    if unhyphenated != word:
        yield unhyphenated

    # Missing spaces seems most common, so check all possible splits first
    if space:
        yield from one_space(word)
    if substitution:
        yield from one_substitution(word)
    if deletion:
        yield from one_deletion(word)
    if insertion:
        yield from one_insertion(word)


def correct_misspelling(given: str,
                        errors=2,
                        space=True,
                        avoid_capitalized_words=False,
                        **kwargs) -> Tuple[bool, str]:
    """Return (bool, guess), True when guess is a known good word."""
    first_letter = given[0]
    rest = given[1:]

    # If it starts with 'I' or 'A', split it if the result is valid.
    if rest and space and first_letter in 'IA' and spellcheck(rest):
        return True, f'{first_letter} {rest}'

    # Ignore other words starting with capital letters
    if avoid_capitalized_words:
        if first_letter.isupper():
            return True, given

    if spellcheck(given):
        return True, given

    # Lazily generate all possible corrections, retuning the first good one.
    def func(words):
        for word in words:
            yield from one_error(word, space=space, **kwargs)
    result_iter = utils.iterate(func, iter([given]), errors)
    candidates: Iterable[str] = itertools.chain.from_iterable(result_iter)
    for word in candidates:
        if spellcheck(word):
            return True, word
    return False, given


def cleanup(given: str, **kwargs) -> str:
    """Return a corrected version of given text."""
    # Re-wrapped text can rejoin lines broken at hyphens, but then you have
    # extra spaces in there, e.g. "mini- mize"
    given = given.replace('- ', '-')
    def silent_fix(wordmatch):
        return correct_misspelling(wordmatch.group(), **kwargs)[1]
    return parse.TOKEN_RE.sub(silent_fix, given)
