#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Cleanup xml text."""

import multiprocessing
from bs4 import BeautifulSoup  # type: ignore

from text_cleanup.raw import cleanup


def reformat(given: str, pretty:bool=False) -> str:
    """Return pretty-formatted version of given."""
    if pretty:
        return BeautifulSoup(given, 'html.parser').prettify()
    return str(BeautifulSoup(given, 'html.parser'))


def clean_element(xml: str, selector=':root',
                  progress_iterator=None, num_processes=1, **kwargs) -> str:
    """Return xml with the selected elements cleaned up. kwargs are passed to
    text_cleanup.raw.cleanup()"""
    # Use html.parser so that it doesn't try to fix the structure
    soup = BeautifulSoup(xml, 'html.parser')
    # Build entire list first to avoid modifying a live iterator
    nodes = set(
        node
        for element in soup.select(selector, **kwargs)
        for node in element.strings
        if not node.isspace())
    if progress_iterator is None:
        progress_iterator = lambda x: x

    text_iterator = map(str, nodes)

    if num_processes > 1:
        with multiprocessing.Pool(num_processes) as pool:
            fixed = []
            futures = [
                pool.apply_async(cleanup, (text,), kwargs)
                for text in text_iterator]
            fixed = [future.get() for future in progress_iterator(futures)]
    else:
        fixed = progress_iterator([cleanup(t, **kwargs) for t in text_iterator])

    for node, new in zip(nodes, fixed):
        _old = node.replace_with(new)
        # Maybe show small diff here?

    return str(soup)
