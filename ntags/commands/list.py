#!/usr/bin/env python
from ..lib.dbclass import DataBase, DEFAULT_TAGDB_FNAME, check_tagdb
from ..lib.color import format_color
def main():
    with DataBase(check_tagdb(DEFAULT_TAGDB_FNAME)) as db:
        for tag, color in db.get_taglist():
            print(format_color(tag, color))
