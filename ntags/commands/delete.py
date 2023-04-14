#!/usr/bin/env python
from ..lib.dbclass import DataBase, DEFAULT_TAGDB_FNAME, check_tagdb
from argparse import ArgumentParser

def main():
    parser = ArgumentParser(description='''A delete command of tag.
ntag-delete [tag]
''')
    parser.add_argument('tag', help='Tag name to delete.')
    args = parser.parse_args()
    with DataBase(check_tagdb(DEFAULT_TAGDB_FNAME)) as db:
        db.delete_tag(args.tag)
