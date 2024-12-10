#!/usr/bin/env python
import argparse
from ..lib.dbclass import DataBase, DEFAULT_TAGDB_FNAME, get_inode, check_tagdb
from ..lib.color import format_color
from ..lib.ninpipe import Pipe
from os.path import exists
import sys


def show_command():
    argparse.ArgumentParser(
        usage='''Command to show tags by path.
Example:
    ls | ntag show''')
    with DataBase(check_tagdb(DEFAULT_TAGDB_FNAME)) as db:
        for data in Pipe().async_iter():
            fname = data.receive()
            if not fname:
                break
            if exists(fname):
                inode = get_inode(fname)
                tags = db.inode2tag(inode)
                ftags = [format_color(*tag) for tag in tags]
                sys.stdout.write(fname)
                ftags = [format_color(*tag) for tag in
                         db.inode2tag(get_inode(fname))]
                sys.stdout.write('[ ')
                sys.stdout.write(' '.join(ftags))
                sys.stdout.write(' ]')
                comment = db.get_comment(inode)
                if comment:
                    sys.stdout.write(': ')
                    sys.stdout.write(comment[0])
                sys.stdout.write('\n')
                sys.stdout.flush()
