#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""Functions for cleaning up text, typically from bad OCR scans."""

import functools
import itertools
import re
import string
import sys

from typing import Any, Tuple, List, Dict, Set, Iterable, Iterator, Callable, TypeVar
A = TypeVar('A')  # pylint: disable=invalid-name
B = TypeVar('B')  # pylint: disable=invalid-name


WORD_PATTERN = r"(?:[\w'-]+)"
NUMBER_PATTERN = r"(?:(?:\d+(?:[.,])?)*\d+)"

TOKEN_RE = re.compile('|'.join((WORD_PATTERN, NUMBER_PATTERN)))
NUMBER_RE = re.compile(NUMBER_PATTERN)

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


def get_valid_words() -> Set[str]:
    """Return set of valid words."""
    with open('words') as fin:
        words = fin.read().splitlines()
    valid: Set[str] = set()
    # Remove one-letter words that aren't 'a', 'A' or 'I'.
    valid.update(w for w in words if len(w) > 1 or w in 'aAI')
    # Allow any word to be capitalized, since it might start a sentence.
    valid.update(w.capitalize() for w in words if w[0].islower())
    return valid
WORDS = get_valid_words()


def spellcheck(wordstr: str) -> bool:
    """Return true if wordstr is made of valid words, else False."""
    quick = (
        wordstr.endswith('-') or
        NUMBER_RE.fullmatch(wordstr) or
        wordstr in WORDS)
    if quick:
        return True
    new = wordstr.replace('-', ' ').split()
    return new[0] != wordstr and all(map(spellcheck, new))


def one_error(word: str) -> Iterable[str]:
    """Yield one-error variations on word."""
    # Missing spaces seems most common, so check all possible splits first
    for i in range(1, len(word)):
        yield word[:i] + ' ' + word[i:]

    # Check for any preferred errors before trying brute force substitution
    for i, letter in enumerate(word):
        for newchar in PREFERRED_ERRORS.get(letter, ''):
            if newchar != letter:
                yield word[:i] + newchar + word[i+1:]

    # No luck... time to brute force
    lower = alpha = string.ascii_lowercase
    upper = string.ascii_uppercase
    for i, letter in enumerate(word):
        # Change letter by trying entire alphabet
        alpha = lower if 'a' <= letter <= 'z' else upper
        for newchar in alpha:
            if newchar != letter:
                yield word[:i] + newchar + word[i+1:]

        # Remove current letter
        yield word[:i] + word[i+1:]

        # Add letter before current letter
        for newchar in alpha:
            yield word[:i] + newchar + word[i:]

    # Add letter at end (reuse final upper vs lower preference)
    for newchar in alpha:
        yield word + newchar


def iterate(func: Callable[[A], A], arg: A,
            iterations=float('inf')) -> Iterable[A]:
    """Yield the successive results of applying func to arg."""
    if hasattr(arg, '__iter__'):
        arg, tmp = itertools.tee(arg)  # type: ignore
    else:
        tmp = arg  # type: ignore
    yield arg
    arg = tmp  # type: ignore
    while iterations > 0:
        iterations -= 1
        arg = func(arg)
        if hasattr(arg, '__iter__'):
            arg, tmp = itertools.tee(arg)  # type: ignore
        else:
            tmp = arg  # type: ignore
        yield arg
        arg = tmp  # type: ignore


def correct_misspelling(given: str, errors=2) -> Tuple[bool, str]:
    """Return (bool, guess), True when guess is a known good word."""
    if spellcheck(given):
        return True, given

    def func(words: Iterator[str]) -> Iterator[str]:
        """partial(flatmap, one_error)... but without confusing mypy."""
        for word in words:
            yield from one_error(word)

    result_iter = iterate(func, iter([given]), errors)
    candidates: Iterable[str] = itertools.chain.from_iterable(result_iter)
    for word in candidates:
        if spellcheck(word):
            return True, word
    return False, given


def cleanup(given: str) -> str:
    """Return a corrected version of given text."""
    # Re-wrapped text can rejoin lines broken at hyphens, but then you have
    # extra spaces in there, e.g. "mini- mize"
    given = given.replace('- ', '-')
    def silent_fix(wordmatch):
        return correct_misspelling(wordmatch.group())[1]
    return TOKEN_RE.sub(silent_fix, given)


def main():
    """Run main."""
    for line in sys.stdin:
        print(cleanup(line), end='')
    return 0

if __name__ == '__main__':
    main()
