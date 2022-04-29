#!/usr/bin/env python
from ..lib.dbclass import print_status, DataBase\
    , find_tagdb_inparents, DEFAULT_TAGDB_FNAME, check_tagdb

def main():
    print_status(
        DataBase(find_tagdb_inparents(check_tagdb(DEFAULT_TAGDB_FNAME)))
    )
