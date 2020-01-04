#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""Functions for cleaning up text, typically from bad OCR scans."""

import string
import itertools
import functools

from typing import Any, Tuple, List, Dict, Set, Iterable, Callable, TypeVar
A = TypeVar('A')  # pylint: disable=invalid-name
B = TypeVar('B')  # pylint: disable=invalid-name
CandidateGroup = Iterable[str]


ERROR_GROUPS = (
    'jli!1t',
    'bdcqeo0@',
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
        words = set(fin.read().splitlines())
    # Remove one-letter words that aren't 'a', 'A' or 'I'.
    words = set(w for w in words if len(w) > 1 or w in 'aAI')
    return words
WORDS = get_valid_words()


def one_space(joined: str) -> Iterable[Tuple[str, str]]:
    """Yield word pairs by splitting `joined` at each letter."""
    for i in range(len(joined)):
        yield (joined[:i], joined[i:])


def one_error(word: str) -> Iterable[CandidateGroup]:
    """Yield lists of one-error variations on word."""
    lower = alpha = string.ascii_lowercase
    upper = string.ascii_uppercase

    for i, letter in enumerate(word):
        # Split into two words before current letter
        if 0 < i < len(word):
            yield [word[:i], word[i:]]

        # Change current letter
        # First check preferred errors
        for newchar in PREFERRED_ERRORS.get(letter, ''):
            if newchar != letter:
                yield [word[:i] + newchar + word[i+1:]]

        # Then try entire alphabet
        alpha = lower if 'a' <= letter <= 'z' else upper
        for newchar in alpha:
            if newchar != letter:
                yield [word[:i] + newchar + word[i+1:]]

        # Remove current letter
        yield [word[:i] + word[i+1:]]

        # Add letter before current letter
        for newchar in alpha:
            yield [word[:i] + newchar + word[i:]]

    # Add letter at end (reuse final upper vs lower preference)
    for newchar in alpha:
        yield [word + newchar]


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


def flatmap(func: Callable[[A], Iterable[A]],
            items: Iterable[A]) -> Iterable[A]:
    """Return concatenated results of map(func, items)."""
    for output in map(func, items):
        yield from output


def correct_misspelling(given: str, errors=2) -> Tuple[bool, str]:
    """Return (bool, guess), indicating whether guess is known good."""
    if given in WORDS:
        return True, given

    def func(words: CandidateGroup) -> Iterable[CandidateGroup]:
        for word in words:
            yield from one_error(word)

    result_iter = iterate(func, [given], errors)
    candidates: Iterable[List[str]] = itertools.chain.from_iterable(result_iter)
    for words in candidates:
        if all(word in WORDS for word in words):
            return True, ' '.join(words)
    return False, given


def main():
    """Run main."""

    return 0

if __name__ == '__main__':
    main()
