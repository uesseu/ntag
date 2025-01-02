from ..lib.dbclass import DataBase, DEFAULT_TAGDB_FNAME, get_inode, check_tagdb
from ..lib.color import format_color
from argparse import ArgumentParser
from sys import stdin, stdout
from stat import ST_INO
from os import stat
from pathlib import Path


def path_command():
    parser = ArgumentParser()
    parser.add_argument('command', help='Sub command.')
    parser.add_argument('path', help='Path')
    parser.add_argument('-a', '--absolute', action='store_true',
                        help='Absolute path.')
    parser.add_argument('-r', '--relative',
                        default='./',
                        help='Relative path from...')
    args = parser.parse_args()

    lines = [
        (n, stat(n)[ST_INO])
        for n
        in stdin.read().splitlines()
    ]

    if stdout.isatty():
        with DataBase(check_tagdb(DEFAULT_TAGDB_FNAME)) as db:
            for n in lines:
                path = Path(n[0]) / args.path
                if args.absolute:
                    path = path.resolve()
                else:
                    path = path.relative_to(args.relative)
                stdout.write(str(path))
                ftags = [format_color(*tag) for tag in
                         db.inode2tag(get_inode(n[0]))]
                stdout.write(' [ ')
                stdout.write(' '.join(ftags))
                stdout.write(' ]')
                stdout.write('\n')
    else:
        for n in lines:
            stdout.write(str(Path(n[0]) / args.path)+'\n')
