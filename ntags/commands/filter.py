#!/usr/bin/env python
from ..lib.dbclass import DataBase, DEFAULT_TAGDB_FNAME, Stat
from ..lib.color import format_color
from ..lib.misc import get_number_unit, set_custom_directory
from ..lib.ninpipe import PipeFname
from pathlib import Path
import sys
from argparse import ArgumentParser


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
    parser.add_argument('-f', '--fileonly', action='store_true',
                        help='Show files only.')
    parser.add_argument('-t', '--dironly', action='store_true',
                        help='Show directories only.')
    parser.add_argument('-u', '--upper', default='', help='Max size of file.')
    parser.add_argument('-l', '--lower', default='',
                        help='Minimum size of file.')
    parser.add_argument('--parent', action='store_true')
    set_custom_directory(parser)
    args = parser.parse_args()

    with DataBase(DEFAULT_TAGDB_FNAME, args.directory if args.relative else '') as db:
        fnames = PipeFname(
            from_glob=sys.stdin.isatty() or args.directory is not None,
            directory=args.directory if args.directory else '.'
        ).async_iter()
        for data in fnames:
            fname = data.receive()
            if not fname:
                break
            path = Path(fname).absolute()
            if not path.exists():
                continue
            if args.dironly and not path.is_dir():
                continue
            if args.fileonly and not path.is_file():
                continue
            stat = Stat(fname)
            upper = get_number_unit(args.upper)
            lower = get_number_unit(args.lower)
            if (
                stat.size > upper.as_byte
                and upper.as_byte != 0
                or stat.size < lower.as_byte
            ):
                continue
            if (
                args.tag
                and not args.invert ^ db.has_tags(stat.inode, args.tag)
            ):
                continue
            sys.stdout.write(fname)
            if sys.stdout.isatty():
                ftags = [
                    format_color(*tag) for tag in
                    db.inode2tag(stat.inode)
                ]
                sys.stdout.write(' [ ')
                sys.stdout.write(' '.join(ftags))
                sys.stdout.write(' ]')
            if args.comment:
                comment = db.get_comment(stat.inode)
                if comment:
                    sys.stdout.write(': ')
                    sys.stdout.write(comment[0])
            sys.stdout.write('\n')
