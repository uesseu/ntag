#!/usr/bin/env python
from ..lib.dbclass import DataBase, DEFAULT_TAGDB_FNAME, check_tagdb
from ..lib.color import format_color
from argparse import ArgumentParser
import sys


def list_command():
    parser = ArgumentParser(usage='''Show list of tags''')
    parser.add_argument('command', help='Sub command.')
    parser.add_argument('-n', '--nocolor', action='store_true')
    parser.add_argument('-s', '--space', action='store_true')
    args = parser.parse_args()
    with DataBase(check_tagdb(DEFAULT_TAGDB_FNAME)) as db:
        if args.space:
            print(' '.join((t for t, c in db.get_taglist() if t)))
            return 0
        for tag, color in db.get_taglist():
            if tag is not None:
                if args.nocolor:
                    print(tag)
                else:
                    print(format_color(tag, color))
