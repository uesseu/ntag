#!/usr/bin/env python
from ..lib.dbclass import (
    print_status, DataBase,
    DEFAULT_TAGDB_FNAME, check_tagdb
)


def status_command(from_root: bool = False):
    print_status(
        DataBase(check_tagdb(DEFAULT_TAGDB_FNAME))
    )
