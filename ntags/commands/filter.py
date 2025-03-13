#!/usr/bin/env python
from ..lib.dbclass import DataBase, DEFAULT_TAGDB_FNAME, get_inode, check_tagdb
from ..lib.color import format_color
from ..lib.ninpipe import Pipe
from os.path import exists
import sys
from argparse import ArgumentParser
from glob import glob
from pathlib import Path

def filter_command() -> None:
    parser = ArgumentParser(
        usage='''File name filter by tag.
If you are using pipe (not from tty), it reads filename from stdin.
If you are not using pipe (and from tty), it reads directory which
you set by option -d. If you did not set -d option, it reads
file names of files of current directory.
Multiple tag names can be set and this means 'or'.
If you want 'and', please run this command twice with pipe.

Options should be set after filter names.

Example.
ls ./*_good.csv | ntag filter good
ntag filter good -d ./
''')
    parser.add_argument('command', help='Sub command.')
    parser.add_argument('tag', nargs='*', help='Tag name to show.')
    parser.add_argument('-v', '--invert', action='store_true',
                        help='Invert flag.')
    parser.add_argument('-c', '--comment', action='store_true',
                        help='With comment.')
    parser.add_argument('--parent', action='store_true')
    parser.add_argument(
        '-d', '--directory', default=None,
        help='Directory path to read.'
        ' This option prevents readlines from stdin.'
    )
    args = parser.parse_args()

    with DataBase(check_tagdb(DEFAULT_TAGDB_FNAME)) as db:
        isatty = sys.stdin.isatty() or args.directory is not None
        directory = args.directory if args.directory else './'
        fnames = glob(directory + '/*') if isatty else Pipe().async_iter()
        for data in fnames:
            fname = data if isatty else data.receive()
            if not fname:
                break
            if not exists(fname):
                continue
            inode = get_inode(fname)
            if args.tag and not args.invert ^ db.has_tags(inode, args.tag):
                continue
            sys.stdout.write(fname)
            if sys.stdout.isatty():
                ftags = [
                    format_color(*tag) for tag in
                    db.inode2tag(get_inode(fname))
                ]
                sys.stdout.write(' [ ')
                sys.stdout.write(' '.join(ftags))
                sys.stdout.write(' ]')
            if args.comment:
                comment = db.get_comment(inode)
                if comment:
                    sys.stdout.write(': ')
                    sys.stdout.write(comment[0])
            sys.stdout.write('\n')
