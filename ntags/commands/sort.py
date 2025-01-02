from ..lib.dbclass import DataBase, DEFAULT_TAGDB_FNAME, get_inode, check_tagdb
from ..lib.color import format_color
from argparse import ArgumentParser
from sys import stdin, stdout
from stat import ST_CTIME, ST_ATIME, ST_MTIME
from os import stat
from glob import glob


def sort_command():
    parser = ArgumentParser(usage='''Sort command of ntag.
In most cases, it get file names from pipe and sort them.
If you did not use pipe, it yields list of file in the
directory and put the result.

Example:
    ntag filter hoge | ntag sort -cv -e -10
    ntag sort -ad ./
''')
    parser.add_argument('command', help='Sub command.')
    parser.add_argument(
        '-c', '--ctime', help='Sort by ctime. Time of last state.',
        action='store_true')
    parser.add_argument(
        '-m', '--mtime', help='Sort by mtime. Time of lat modification.',
        action='store_true')
    parser.add_argument(
        '-a', '--atime', help='Sort by atime. Time of last access.',
        action='store_true')
    parser.add_argument(
        '-s', '--start', help='Start of the items. It can be less than -1',
        type=int, default=0)
    parser.add_argument(
        '-e', '--end', help='End of the items. It can be less than -1.',
        type=int, default=0)
    parser.add_argument(
        '-d', '--directory', help='Directory to look.',
        default='./')
    parser.add_argument(
        '-v', '--invert', help='Invert the sort',
        action='store_true')
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
        (n, stat(n)[st_time]) for n in
        (glob(args.directory + '/*') if stdin.isatty
         else stdin.read().splitlines())
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
