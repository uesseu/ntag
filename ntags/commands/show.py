#!/usr/bin/env python
import argparse
from ..lib.dbclass import DataBase, DEFAULT_TAGDB_FNAME, get_inode, check_tagdb
from ..lib.color import format_color
from ..lib.ninpipe import Pipe
from os.path import exists


def show_command(from_root: bool = False):
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
                tags = db.inode2tag(get_inode(fname))
                ftags = [format_color(*tag) for tag in tags]
                print(fname, '[', ' '.join(ftags), ']')
