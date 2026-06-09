#!/usr/bin/env python
from ..lib.color import format_color
from ..lib.dbclass import (
    print_status, DataBase,
    DEFAULT_TAGDB_FNAME
)
from ..lib.misc import set_custom_directory
from argparse import ArgumentParser


def status_command():
    parser = ArgumentParser(
        usage='''Show status of ntag.'''
    )
    parser.add_argument('command')
    set_custom_directory(parser)
    args = parser.parse_args()
    print_status(
        DataBase(DEFAULT_TAGDB_FNAME, args.directory if args.relative else '')
    )
    print('List of tags')
    with DataBase(DEFAULT_TAGDB_FNAME, args.directory if args.relative else '') as db:
        for tag, color in db.get_taglist():
            if tag is not None:
                print(' ' * 2 + format_color(tag, color))
