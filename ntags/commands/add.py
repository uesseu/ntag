#!/usr/bin/env python
from pathlib import Path
from ..lib.dbclass import DataBase, get_inode, DEFAULT_TAGDB_FNAME, check_tagjson
from ..lib.ninpipe import Pipe
from ..lib.defaults import DEFAULT_TAGJSON_FNAME
from ..lib.misc import set_custom_directory
from argparse import ArgumentParser
import sys


def add_command():
    parser = ArgumentParser(
        usage='''Add a tag to file.
It reads fname from stdin.
If there is no tags

Example.
ls ./*_good.csv | ntag-add good new''')
    parser.add_argument('command', help='Sub command of ntag.')
    parser.add_argument(
        'tag', nargs='*', action="extend",
        type=str, help='Tag name to delete.'
    )
    parser.add_argument(
        '-p', '--path', action="store_true", help='Path based.'
    )
    set_custom_directory(parser)
    isatty = sys.stdin.isatty()
    if isatty:
        parser.add_argument(
            '-f', '--file', default='./',
            help='File name'
        )
    args = parser.parse_args()
    if args.path:
        tagjson = check_tagjson(DEFAULT_TAGJSON_FNAME, '')
        if tagjson:
            import json
            data = json.loads(Path(tagjson).read_text())
            if isatty:
                path = [str(Path(args.file).resolve())]
            else:
                path = [str(Path(p).resolve()) for p in Pipe()]
            for p in path:
                print(p)
                if p in data:
                    data[p]['tag'] += args.tag
                else:
                    data[p]['tag'] = args.tag
            Path(tagjson).write_text(json.dumps(data))
        return 0

    with DataBase(DEFAULT_TAGDB_FNAME, args.directory and args.relative) as db:
        if isatty:
            for tag in args.tag:
                db.add_tag(get_inode(args.file), tag)
        else:
            for fname in Pipe():
                for tag in args.tag:
                    db.add_tag(get_inode(fname), tag)
