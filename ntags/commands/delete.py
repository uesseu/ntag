#!/usr/bin/env python
from pathlib import Path
from ..lib.ninpipe import Pipe
from ..lib.dbclass import DataBase, DEFAULT_TAGDB_FNAME, check_tagjson
from ..lib.defaults import DEFAULT_TAGJSON_FNAME
from argparse import ArgumentParser


def delete_command():
    parser = ArgumentParser(
        usage='''Just delete tag.

Example.
# Delete tag named "hoge".
ntag delete hoge''')
    parser.add_argument('command', help='Sub command.')
    parser.add_argument('tag', help='Tag name to delete.')
    args = parser.parse_args()

    with DataBase(DEFAULT_TAGDB_FNAME, args.directory if args.relative else '') as db:
        db.delete_tag(args.tag)
