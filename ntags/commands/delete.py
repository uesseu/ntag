#!/usr/bin/env python
from ..lib.dbclass import DataBase, DEFAULT_TAGDB_FNAME, check_tagdb
from argparse import ArgumentParser


def delete_command(from_root: bool = False):
    parser = ArgumentParser(
        usage='''A delete command of tag.
ntag-delete [tag]
''')
    if from_root:
        parser.add_argument('command', help='Sub command of ntag.')
    parser.add_argument('tag', help='Tag name to delete.')
    args = parser.parse_args()
    with DataBase(check_tagdb(DEFAULT_TAGDB_FNAME)) as db:
        db.delete_tag(args.tag)
