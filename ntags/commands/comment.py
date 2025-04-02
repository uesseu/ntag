#!/usr/bin/env python
from ..lib.dbclass import DataBase, get_inode, check_tagdb, DEFAULT_TAGDB_FNAME
from ..lib.ninpipe import Pipe, PipeFname
from argparse import ArgumentParser
from os.path import exists
import sys


def addcomment_command():
    parser = ArgumentParser(
        usage='''Add a comment to file.
It reads fname from stdin.
If there is no tags

Example.
ls ./*_good.csv | ntag add_comment 'It is a special file.' ''')
    parser.add_argument('command', help='Sub command of ntag.')
    parser.add_argument('comment', type=str, help='Comment.')
    parser.add_argument(
        '-d', '--directory', default=None,
        help='Directory path to read.'
        ' This option prevents readlines from stdin.'
    )
    args = parser.parse_args()
    with DataBase(check_tagdb(DEFAULT_TAGDB_FNAME)) as db:
        for fname in Pipe():
            if exists(fname):
                db.add_comment(get_inode(fname), args.comment)


def getcomment_command():
    parser = ArgumentParser(
        usage='''Command to show tags by path.
Example:
    ls | ntag get_comment''')
    parser.add_argument('command')
    parser.add_argument(
        '-d', '--directory', default=None,
        help='Directory path to read.'
        ' This option prevents readlines from stdin.'
    )
    args = parser.parse_args()
    with DataBase(check_tagdb(DEFAULT_TAGDB_FNAME)) as db:
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
Example:
    ls | ntag filter_comment hoge''')
    parser.add_argument('command')
    parser.add_argument('keywords')
    parser.add_argument(
        '-d', '--directory', default=None,
        help='Directory path to read.'
        ' This option prevents readlines from stdin.'
    )
    args = parser.parse_args()

    with DataBase(check_tagdb(DEFAULT_TAGDB_FNAME)) as db:
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
            if args.keywords in comment:
                sys.stdout.write(fname)
                sys.stdout.write('\n')
                sys.stdout.flush()


