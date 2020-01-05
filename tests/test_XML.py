#!/usr/bin/env python
# -*- coding: utf-8 -*-
# type: ignore
# pylint: disable=missing-docstring,invalid-name
"""Test xml cleaning code."""

import unittest

from text_cleanup import XML


class TestXMLHandling(unittest.TestCase):
    """Just handle extracting and modifying text within XML."""

    def setUp(self):
        self.big_xml = XML.reformat(open('tests/sample.xml').read().strip())
        self.small_xml = XML.reformat("""
          <body dir="auto">
            <h1 dir="ltr" class="center">
              Stranger In A Strange Land
            </h1>
            <p dir="ltr" class="center bold">
              Robert Heinlein
            </p>
            <div class="offset">
              <p dir="ltr">
                This book was produced in EPUB format by the Internet Archive.
              </p>
            </div>
          </body>
        """.strip())

    def test_simple_cleanup(self):
        xml = "<div>Balogna</div>"
        expected = xml.replace("Balogna", "Bologna")
        result = XML.clean_element(xml, 'div')
        self.assertEqual(result, expected)

    def test_scary_cleanup(self):
        xml = self.small_xml.replace('produced', 'pridoced')
        xml = xml.replace('In A', 'InA')
        expected = self.small_xml
        result = XML.clean_element(xml)
        self.assertEqual(result, expected)

    def test_dont_touch_attribute_values(self):
        xml      = '<div class="bal1s">Bal1s.</div>'
        expected = '<div class="bal1s">Balls.</div>'
        result = XML.clean_element(xml)
        self.assertEqual(result, expected)

    def test_only_fix_selected(self):
        xml      = '<div class="bal1s">Bal1s.</div><div>Bal1s</div>'
        expected = '<div class="bal1s">Balls.</div><div>Bal1s</div>'
        result = XML.clean_element(xml, selector='.bal1s')
        self.assertEqual(result, expected)


if __name__ == '__main__':
    unittest.main()
