from glob import glob
from ..lib.dbclass import DataBase, get_inode, check_tagdb, DEFAULT_TAGDB_FNAME
from ..lib.ninpipe import Pipe
from sys import stdin
import json

def export_command():
    flist = list(glob('**', recursive=True))
    result = {}
    fname_dict = {}
    tag_dict = {}
    with DataBase(check_tagdb(DEFAULT_TAGDB_FNAME)) as db:
        for fname in flist:
            tags = db.inode2tag(get_inode(fname))
            for tag in tags:
                if tag[0] in fname_dict:
                    fname_dict[tag[0]].append(fname)
                else:
                    fname_dict.update({tag[0]: [fname]})
        print(json.dumps({'tags': list(db.get_taglist()), 'files': fname_dict}))


def import_command():
    db_json = json.loads(stdin.read())
    fname_dict = db_json['files']
    tags = db_json['tags']
    with DataBase(check_tagdb(DEFAULT_TAGDB_FNAME)) as db:
        for key, value in tags:
            db.make_new_tag(key, value)
        for key, values in fname_dict.items():
            for value in values:
                with DataBase(check_tagdb(DEFAULT_TAGDB_FNAME)) as db:
                    db.add_tag(get_inode(value), key)
