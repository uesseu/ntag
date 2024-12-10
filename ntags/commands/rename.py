#!/usr/bin/env python
from ..lib.dbclass import DataBase, DEFAULT_TAGDB_FNAME, check_tagdb
from ..lib.misc import get_tag_from_arg


def rename_command():
    parser = ArgumentParser(
        usage='''Rename tag.

Example.
# Rename tag named hoge to fuga
> ntag rename hoge fuga''')
    parser.add_argument('command', help='Sub command.')
    parser.add_argument('tag', help='Tag name to delete.')
    args = parser.parse_args()

    with DataBase(check_tagdb(DEFAULT_TAGDB_FNAME)) as db:
        db.rename_tag(tag, input())
