#!/usr/bin/env python
from ..lib.dbclass import DataBase, DEFAULT_TAGDB_FNAME


def init_command(from_root: bool = False):
    db = DataBase(DEFAULT_TAGDB_FNAME)
    db.close()
