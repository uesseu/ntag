from ..lib.dbclass import DataBase, get_inode, check_tagdb, DEFAULT_TAGDB_FNAME
from sys import stdin
import json
from multiprocessing import Pool
import os
from itertools import chain


def _get_inode_fname(data):
    paths = [os.path.join(data[0], p) for p in data[1]]\
        + [os.path.join(data[0], p) for p in data[2]]
    return [(get_inode(path), path) for path in paths]


def export_command():
    fname_dict = {}
    with DataBase(check_tagdb(DEFAULT_TAGDB_FNAME)) as db:
        with Pool(min(os.cpu_count(), 8)) as p:
            inode_file_list = p.map(_get_inode_fname, os.walk('.'))
        for inode, fname in chain.from_iterable(inode_file_list):
            tags = db.inode2tag(inode)
            for tag in tags:
                if tag[0] in fname_dict:
                    fname_dict[tag[0]].append(fname)
                else:
                    fname_dict.update({tag[0]: [fname]})
        print(json.dumps(
            {'tags': list(db.get_taglist()), 'files': fname_dict}
        ))


def import_command():
    db_json = json.loads(stdin.read())
    fname_dict = db_json['files']
    tags = db_json['tags']
    with DataBase(check_tagdb(DEFAULT_TAGDB_FNAME)) as db:
        for key, value in tags:
            db.make_new_tag(key, value)
        for key, values in fname_dict.items():
            for value in values:
                db.add_tag(get_inode(value), key)
