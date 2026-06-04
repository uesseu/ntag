#!/usr/bin/env python
from ..lib.dbclass import DataBase, DEFAULT_TAGDB_FNAME
from ..lib.ninpipe import Pipe
from ..lib.misc import EXCLUDEDCHAR
from argparse import ArgumentParser
import sys


def make_command():
    parser = ArgumentParser(
            usage='''Make tag.
    Please write tag name!

    Example.
    echo hoge | ntag make''')
    parser.add_argument('command', help='Sub command of ntag.')
    parser.parse_args()

    if sys.stdin.isatty():
        print('Please enter a name of tag.')
    tagname = next(Pipe()).strip()

    for exe in EXCLUDEDCHAR:
        if exe in tagname:
            raise Exception('You can not put such characters like ', EXCLUDEDCHAR)

    with DataBase(DEFAULT_TAGDB_FNAME, args.directory if args.relative else '') as db:
        db.make_new_tag(tagname)
