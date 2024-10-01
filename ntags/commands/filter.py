#!/usr/bin/env python
from ..lib.dbclass import DataBase, DEFAULT_TAGDB_FNAME, get_inode, check_tagdb
from ..lib.color import format_color
from ..lib.ninpipe import Pipe
from ..lib.misc import get_tag_from_arg
from os.path import exists
import sys
from argparse import ArgumentParser


def filter_command(from_root: bool = False) -> None:
    parser = ArgumentParser(
        usage='''Add a tag to file.
It reads fname from stdin.

Example.
ls ./*_good.csv | ntag-filter good | column''')
    parser.add_argument('tag', help='Tag name to delete.')
    args = parser.parse_args()

    args.tag = get_tag_from_arg('> ntag-add [tag]')
    with DataBase(check_tagdb(DEFAULT_TAGDB_FNAME)) as db:
        for data in Pipe().async_iter():
            fname = data.receive()
            if not fname:
                break
            if not exists(fname):
                continue
            inode = get_inode(fname)
            if not db.has_tags(inode, args.tag.split(',')):
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
