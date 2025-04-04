#!/usr/bin/env python
from ..lib.dbclass import DataBase, DEFAULT_TAGDB_FNAME, check_tagdb
from ..lib.ninpipe import Pipe
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
    tagname = next(Pipe())
    with DataBase(check_tagdb(DEFAULT_TAGDB_FNAME)) as db:
        db.make_new_tag(tagname)
