#!/usr/bin/env python
from ..lib.dbclass import DataBase, DEFAULT_TAGDB_FNAME
from ..lib.misc import get_tag_from_arg


def rename_command():
    parser = ArgumentParser(
        usage='''Rename tag.

Example.
# Rename tag named hoge to fuga
> ntag rename hoge fuga''')
    parser.add_argument('command', help='Sub command.')
    parser.add_argument('tag', help='Tag name to rename.')
    args = parser.parse_args()

    with DataBase(DEFAULT_TAGDB_FNAME, args.directory if args.relative else '') as db:
        db.rename_tag(tag, input())
