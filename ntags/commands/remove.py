#!/usr/bin/env python
from ..lib.dbclass import DataBase, DEFAULT_TAGDB_FNAME, get_inode, check_tagdb
from ..lib.ninpipe import Pipe
from ..lib.misc import get_tag_from_arg


def remove_command(from_root: bool = False):
    tag = get_tag_from_arg(
        '> ntag-remove [tag]',
        from_root=from_root
    )
    with DataBase(check_tagdb(DEFAULT_TAGDB_FNAME)) as db:
        for fname in Pipe():
            db.remove_tag_from_inode(tag, get_inode(fname))
