#!/usr/bin/env python
from ..lib.dbclass import DataBase, get_inode, check_tagdb, DEFAULT_TAGDB_FNAME
from ..lib.ninpipe import Pipe
from argparse import ArgumentParser


def add_command(from_root: bool = False):
    parser = ArgumentParser(
        usage='''Add a tag to file.
It reads fname from stdin.
If there is no tags

Example.
ls ./*_good.csv | ntag-add good new''')
    parser.add_argument('command', help='Sub command of ntag.')
    parser.add_argument(
        'tag', nargs='*', action="extend",
        type=str, help='Tag name to delete.'
    )
    args = parser.parse_args()
    with DataBase(check_tagdb(DEFAULT_TAGDB_FNAME)) as db:
        for fname in Pipe():
            for tag in args.tag:
                db.add_tag(get_inode(fname), tag)
