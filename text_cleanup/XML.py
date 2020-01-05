#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Cleanup xml text."""

from bs4 import BeautifulSoup  # type: ignore
from text_cleanup.raw import cleanup


def reformat(given: str, pretty=False) -> str:
    """Return pretty-formatted version of given."""
    if pretty:
        return BeautifulSoup(given, 'html.parser').prettify()
    return str(BeautifulSoup(given, 'html.parser'))


def clean_element(xml: str, selector=':root', **kwargs) -> str:
    """Return xml with the selected elements cleaned up. kwargs are passed to
    BeautifulSoup.select()"""
    # Use html.parser so that it doesn't try to fix the structure
    soup = BeautifulSoup(xml, 'html.parser')
    for element in soup.select(selector, **kwargs):
        # Build entire list first to avoid modifying a live iterator
        for text in list(element.strings):
            if not text.isspace():
                _old = text.replace_with(cleanup(str(text)))
            # Maybe show small diff here?
    return str(soup)
