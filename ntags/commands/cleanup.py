#!/usr/bin/env python
from ..lib.dbclass import DataBase, get_inode, DEFAULT_TAGDB_FNAME
from argparse import ArgumentParser
from multiprocessing import Pool
import os
from itertools import chain


def _get_inode_fname(data):
    paths = [os.path.join(data[0], p) for p in data[1]]\
        + [os.path.join(data[0], p) for p in data[2]]
    return [(get_inode(path), path) for path in paths]


def cleanup_command():
    ArgumentParser(
        usage='''Remove unused tags.

Example.
ntag cleanup
''')
    fname_dict = {}
    with DataBase(DEFAULT_TAGDB_FNAME) as db:
        with Pool(min(os.cpu_count(), 8)) as p:
            inode_file_list = p.map(_get_inode_fname, os.walk('.'))
        for inode, fname in chain.from_iterable(inode_file_list):
            tags = db.inode2tag(inode)
            for tag in tags:
                if tag[0] in fname_dict:
                    fname_dict[tag[0]].append(fname)
                else:
                    fname_dict.update({tag[0]: [fname]})
        keys = list(fname_dict.keys())
        taglist = list(db.get_taglist())
        for tag, _ in taglist:
            if tag not in keys:
                print(f'deleting [{tag}]')
                db.delete_tag(tag)
