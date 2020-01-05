#!/usr/bin/env python
# -*- coding: utf-8 -*-

import itertools

from typing import Any, Tuple, List, Dict, Set, Iterable, Iterator, Callable, TypeVar
A = TypeVar('A')  # pylint: disable=invalid-name
B = TypeVar('B')  # pylint: disable=invalid-name


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


def flatmap(func: Callable[[Iterator[A]], Iterator[Iterator[A]]],
            items: Iterator[A]) -> Iterator[A]:
    """Return concatenated result of mapping func over items."""
    for item in items:
        yield from func(item)

