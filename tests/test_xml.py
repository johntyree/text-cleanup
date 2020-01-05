#!/usr/bin/env python
# -*- coding: utf-8 -*-
# type: ignore
# pylint: disable=missing-docstring
"""Test xml cleaning code."""

import unittest

from text_cleanup import xml


class TestXMLHandling(unittest.TestCase):
    """Just handle extracting and modifying text within XML."""

    def setUp(self):
        self.big_xml = open('tests/sample.xml').read()
        self.small_xml = """
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
        """

    def tist_getnodes(self):
        nodes = xml.get_nodes(self.small_xml)
        self.assertEqual(len(nodes), 4)


if __name__ == '__main__':
    unittest.main()
