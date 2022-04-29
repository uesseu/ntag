#!/usr/bin/env python
from ..lib.dbclass import DataBase, DEFAULT_TAGDB_FNAME
def main():
    db = DataBase(DEFAULT_TAGDB_FNAME)
    db.close()
