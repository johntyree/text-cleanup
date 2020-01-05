#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import argparse


def main(argv):
    parser = argparse.ArgumentParser("Clean up text.")
    parser.add_argument(
        '-i', type=str, help="The input file to clean up.", default='-')
    parser.add_argument(
        '--selector',
        help="Only clean elements mathching this CSS selector. Implies --xml.")
    parser.add_argument('--xml', action='store_true', help="Assume XML input.")
    group = parser.add_mutually_exclusive_group()
    group.add_argument(
        '--reformat-only', action='store_true',
        help="Prettify XML input without changing any of the text.")
    args = parser.parse_args(argv)
    print(args)


if __name__ == '__main__':
    main(sys.argv)
