#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Entry point for text-cleanup cli."""

import sys
import argparse
import progressbar

from text_cleanup import raw, XML


def main(argv=None):
    """Entry point for text-cleanup cli."""
    parser = argparse.ArgumentParser("Clean up text.")
    parser.add_argument(
        'input', type=argparse.FileType(encoding='utf-8'),
        help="The input file to clean up.", default=sys.stdin)
    parser.add_argument(
        '--output', type=argparse.FileType(encoding='utf-8'),
        help="Write results to this filename.", default=sys.stdout)
    parser.add_argument(
        '--selector', '-s',
        help="Only clean elements mathching this CSS selector. Implies --xml.")
    parser.add_argument('--xml', action='store_true', help="Assume XML input.")
    parser.add_argument('--num_processes', '-n', metavar='N',
                        help="Utilize N processes.", type=int, default=1)
    group = parser.add_mutually_exclusive_group()
    group.add_argument(
        '--reformat-only', action='store_true',
        help="Prettify XML input without changing any of the text.")

    args = parser.parse_args(argv or sys.argv[1:])

    # Fix dependencies between arguments (e.g. x implies y)
    if args.selector or args.reformat_only:
        args.xml = True
    if args.selector is None:
        args.selector = ':root'

    if args.xml:
        xml = args.input.read()
        if args.reformat_only:
            output = XML.reformat(xml)
        else:
            def make_bar(items):
                return progressbar.progressbar(items)
            output = XML.clean_element(
                xml, args.selector, progress_iterator=make_bar,
                num_processes=args.num_processes,
            )
    else:
        text = args.input.read()
        output = raw.cleanup(text)

    args.output.write(output)


if __name__ == '__main__':
    main()
