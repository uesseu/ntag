#!/usr/bin/env python
from ..lib.dbclass import (
    DataBase, get_inode, DEFAULT_TAGDB_FNAME, check_tagjson, DEFAULT_TAGJSON_FNAME
)
from ..lib.ninpipe import Pipe, PipeFname
from ..lib.misc import set_custom_directory
from argparse import ArgumentParser
from os.path import exists
import sys
from pathlib import Path
tagjson = check_tagjson(DEFAULT_TAGJSON_FNAME)


def addcomment_command():
    parser = ArgumentParser(
        usage='''Add a comment to file.
It reads fname from stdin.
If there is no tags

Example.
ls ./*_good.csv | ntag add_comment 'It is a special file.' ''')
    parser.add_argument('command', help='Sub command of ntag.')
    parser.add_argument('comment', type=str, help='Comment.')
    set_custom_directory(parser)
    args = parser.parse_args()
    with DataBase(DEFAULT_TAGDB_FNAME, args.directory and args.relative) as db:
        for fname in Pipe():
            if exists(fname):
                db.add_comment(get_inode(fname), args.comment)


def getcomment_command():
    parser = ArgumentParser(
        usage='''Command to show tags by path.
Example:
    ls | ntag get_comment''')
    parser.add_argument('command')
    set_custom_directory(parser)
    args = parser.parse_args()
    with DataBase(DEFAULT_TAGDB_FNAME, args.directory if args.relative else '') as db:
        fnames = PipeFname(
            from_glob=sys.stdin.isatty() or args.directory is not None,
            directory=(args.directory + '/*') if args.directory else './*'
        ).async_iter()
        for data in fnames:
            fname = data.receive()
            if not fname:
                break
            if not exists(fname):
                continue
            comment = db.get_comment(get_inode(fname))
            comment = comment[0] if comment else ''
            sys.stdout.write(comment)
            sys.stdout.write('\n')
            sys.stdout.flush()


def filtercomment_command():
    parser = ArgumentParser(
        usage='''Filter by comment.
The comment will be filterd by regex.

Example:
    ls | ntag filter_comment hoge''')
    parser.add_argument('command')
    parser.add_argument('keywords')
    set_custom_directory(parser)
    args = parser.parse_args()
    import re
    regex = re.compile(args.keywords)

    if tagjson:
        import json
        path_tags = json.loads(Path(tagjson).read_text())
    with DataBase(DEFAULT_TAGDB_FNAME) as db:
        fnames = PipeFname(
            from_glob=sys.stdin.isatty() or args.directory is not None,
            directory=(args.directory) if args.directory else ''
        ).async_iter()
        for data in fnames:
            fname = data.receive()
            if not fname:
                break
            if not exists(fname):
                continue
            if tagjson:
                try:
                    if (path_tags[str(Path(fname).resolve())]['comment']):
                        sys.stdout.write(fname)
                        sys.stdout.write('\n')
                        sys.stdout.flush()
                        continue
                except:
                    pass
            comment = db.get_comment(get_inode(fname))
            comment = comment[0] if comment else ''
            if not regex.search(comment):
                continue
            sys.stdout.write(fname)
            sys.stdout.write('\n')
            sys.stdout.flush()

