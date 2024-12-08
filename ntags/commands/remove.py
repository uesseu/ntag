#!/usr/bin/env python
from ..lib.dbclass import DataBase, DEFAULT_TAGDB_FNAME, get_inode, check_tagdb
from ..lib.ninpipe import Pipe
from argparse import ArgumentParser
from sys import stdin


def remove_command():
    parser = ArgumentParser(
        usage='''Remove tag from files.
The file names should be read from stdin.

Example.
# Delete all the tag named "hoge".
ls | ntag filter tag-name | ntag remove tag-name
ntag remove tag-name file-name''')
    parser.add_argument('command', help='Sub command.')
    parser.add_argument(
        'tag', nargs='*', action="extend",
        type=str, help='Tag name to delete.'
    )
    if stdin.isatty():
        parser.add_argument('fname', help='File name which has tag.')
    args = parser.parse_args()
    if stdin.isatty():
        fname = args.fname
        with DataBase(check_tagdb(DEFAULT_TAGDB_FNAME)) as db:
            for tag in args.tag:
                db.remove_tag_from_inode(tag, get_inode(fname))
    else:
        with DataBase(check_tagdb(DEFAULT_TAGDB_FNAME)) as db:
            for fname in Pipe():
                for tag in args.tag:
                    db.remove_tag_from_inode(tag, get_inode(fname))
