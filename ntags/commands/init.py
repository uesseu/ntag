#!/usr/bin/env python
from ..lib.dbclass import DataBase, DEFAULT_TAGDB_FNAME, check_tagdb
from argparse import ArgumentParser


def init_command(from_root: bool = False):
    parser = ArgumentParser(
            usage='''Make tag database in current directory.
    This command makes sqlite database named '.nintag_db'.

    Example.
    ntag init''')
    parser.add_argument('command', help='Sub command of ntag.')
    parser.parse_args()

    db = DataBase(check_tagdb(DEFAULT_TAGDB_FNAME))
    db.close()
