#!/usr/bin/env python
# -*- coding: utf-8 -*-

import re

WORD_PATTERN = r"(?:[\w'-]+)"
NUMBER_PATTERN = r"(?:(?:\d+(?:[.,])?)*\d+)"

TOKEN_RE = re.compile('|'.join((WORD_PATTERN, NUMBER_PATTERN)))
NUMBER_RE = re.compile(NUMBER_PATTERN)
