#!/usr/bin/env python
from pathlib import Path
from ..lib.defaults import DEFAULT_TAGJSON_FNAME
from ..lib.dbclass import DataBase, DEFAULT_TAGDB_FNAME, get_inode, check_tagjson
from ..lib.ninpipe import Pipe
from ..lib.misc import set_custom_directory
from argparse import ArgumentParser
from sys import stdin


def remove_command():
    parser = ArgumentParser(
        usage='''Remove tag from files.
The file names should be read from stdin.

Example.
Delete tag named "hoge" from path.

ls | ntag filter tag-name | ntag remove tag-name
ntag remove tag-name file-name''')
    parser.add_argument('command', help='Sub command.')
    parser.add_argument(
        'tag', nargs='*', action="extend",
        type=str, help='Tag name to delete.'
    )
    parser.add_argument(
        '-p', '--path', action="store_true",
        help='Path based tag.'
    )

    if stdin.isatty():
        parser.add_argument('fname', help='File name which has tag.')
    set_custom_directory(parser)
    args = parser.parse_args()

    if args.path:
        tagjson = check_tagjson(DEFAULT_TAGJSON_FNAME, '')
        if tagjson:
            import json
            data = json.loads(Path(tagjson).read_text())
            if stdin.isatty():
                path = [str(Path(args.fname).resolve())]
            else:
                path = [str(Path(p).resolve()) for p in Pipe()]
            for p in path:
                if p in data:
                    for tag in args.tag:
                        if tag in data[p]['tag']:
                            del data[p]['tag'][data[p]['tag'].index(tag)]
            Path(tagjson).write_text(json.dumps(data, indent=2))
        return 0

    if stdin.isatty():
        fname = args.fname
        with DataBase(DEFAULT_TAGDB_FNAME, args.directory if args.relative else '') as db:
            for tag in args.tag:
                db.remove_tag_from_inode(tag, get_inode(fname))
    else:
        with DataBase(DEFAULT_TAGDB_FNAME, args.directory if args.relative else '') as db:
            for fname in Pipe():
                for tag in args.tag:
                    db.remove_tag_from_inode(tag, get_inode(fname))
