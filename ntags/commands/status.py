#!/usr/bin/env python
from ..lib.color import format_color
from ..lib.dbclass import (
    print_status, DataBase,
    DEFAULT_TAGDB_FNAME, check_tagdb
)


def status_command():
    print_status(
        DataBase(check_tagdb(DEFAULT_TAGDB_FNAME))
    )
    print('List of tags')
    with DataBase(check_tagdb(DEFAULT_TAGDB_FNAME)) as db:
        for tag, color in db.get_taglist():
            if tag is not None:
                print(' ' * 2 + format_color(tag, color))
