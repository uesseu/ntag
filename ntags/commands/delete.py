#!/usr/bin/env python
from ..lib.dbclass import DataBase, DEFAULT_TAGDB_FNAME, check_tagdb
from ..lib.misc import get_tag_from_arg
def main():
    tag = get_tag_from_arg('> ntag-delete [tag]')
    with DataBase(check_tagdb(DEFAULT_TAGDB_FNAME)) as db:
        db.delete_tag(tag)
