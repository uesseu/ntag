#!/usr/bin/env python
from ..lib.dbclass import DataBase, DEFAULT_TAGDB_FNAME, check_tagdb
from ..lib.ninpipe import Pipe
def main():
    tagname = next(Pipe())
    with DataBase(check_tagdb(DEFAULT_TAGDB_FNAME)) as db:
        db.make_new_tag(tagname)
