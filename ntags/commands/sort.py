from ..lib.dbclass import DataBase, DEFAULT_TAGDB_FNAME, get_inode, check_tagdb
from ..lib.color import format_color
from argparse import ArgumentParser
from sys import stdin, stdout
from stat import ST_CTIME, ST_ATIME, ST_MTIME
from os import stat


def sort_command():
    parser = ArgumentParser()
    parser.add_argument('command', help='Sub command.')
    parser.add_argument('-c', '--ctime', action='store_true')
    parser.add_argument('-m', '--mtime', action='store_true')
    parser.add_argument('-a', '--atime', action='store_true')
    parser.add_argument('-s', '--start', type=int, default=0)
    parser.add_argument('-e', '--end', type=int, default=0)
    parser.add_argument('-v', '--invert', action='store_true')
    args = parser.parse_args()

    st_time: int | None = None
    if args.ctime:
        st_time = ST_CTIME
    if args.atime:
        st_time = ST_ATIME
    if args.mtime:
        st_time = ST_MTIME
    if st_time is None:
        st_time = ST_MTIME

    lines = [
        (n, stat(n)[st_time])
        for n
        in stdin.read().splitlines()
    ]

    result = [
        n[0]
        for n
        in sorted(lines, key=lambda x: x[1], reverse=args.invert)
    ][args.start:len(lines)-args.end]
    if stdout.isatty():
        with DataBase(check_tagdb(DEFAULT_TAGDB_FNAME)) as db:
            for n in result:
                stdout.write(n)
                ftags = [format_color(*tag) for tag in
                         db.inode2tag(get_inode(n))]
                stdout.write(' [ ')
                stdout.write(' '.join(ftags))
                stdout.write(' ]')
                stdout.write('\n')
    else:
        for n in result:
            stdout.write(n+'\n')
