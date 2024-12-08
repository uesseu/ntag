#!/usr/bin/env python
from ..lib.dbclass import DataBase, DEFAULT_TAGDB_FNAME, get_inode, check_tagdb
from ..lib.color import format_color
from ..lib.ninpipe import Pipe
from os.path import exists
import sys
from argparse import ArgumentParser


def filter_command() -> None:
    parser = ArgumentParser(
        usage='''Filter by tag.
It reads fname from stdin.

Example.
ls ./*_good.csv | ntag-filter good | column''')
    parser.add_argument('command', help='Sub command.')
    parser.add_argument('-v', default=False, help='Invert flag.')
    parser.add_argument('tag', nargs='+', help='Tag name to show.')
    args = parser.parse_args()

    with DataBase(check_tagdb(DEFAULT_TAGDB_FNAME)) as db:
        for data in Pipe().async_iter():
            fname = data.receive()
            if not fname:
                break
            if not exists(fname):
                continue
            inode = get_inode(fname)
            if not args.v ^ db.has_tags(inode, args.tag):
                continue
            sys.stdout.write(fname)
            if sys.stdout.isatty():
                ftags = [format_color(*tag) for tag in
                         db.inode2tag(get_inode(fname))]
                sys.stdout.write('[ ')
                sys.stdout.write(' '.join(ftags))
                sys.stdout.write(' ]')
            sys.stdout.write('\n')
            sys.stdout.flush()
