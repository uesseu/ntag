#!/usr/bin/env python
from ..lib.dbclass import DataBase, get_inode, check_tagdb, DEFAULT_TAGDB_FNAME
from ..lib.ninpipe import Pipe
from ..lib.misc import get_tag_from_arg
def main():
    tag = get_tag_from_arg('> ntag-add [tag]')
    with DataBase(check_tagdb(DEFAULT_TAGDB_FNAME)) as db:
        for fname in Pipe():
            db.add_tag(get_inode(fname), tag)