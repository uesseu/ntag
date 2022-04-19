import sqlite3
from typing import List, cast, Any, Optional
from os.path import exists
from logging import getLogger, INFO, DEBUG
from pathlib import Path
from sys import stderr
from os import stat, environ
from stat import ST_INO
logger = getLogger()
logger.setLevel(INFO)
db_fname: str = f'{environ["HOME"]}/.config/nintag/nintag.db'

def get_inode(path: Path) -> int:
    return stat(path)[ST_INO]

def read_pipe() -> List[str]:
    file_list = []
    while True:
        try:
            result = input()
            if result == '':
                raise EOFError()
            file_list.append(result)
        except EOFError:
            return file_list

class DB:
    def __init__(self, fname: str):
        self.fname = fname
        self._to_make_new: bool = False if exists(fname) else True
        if not Path(db_fname).parent.exists():
            raise FileNotFoundError(f'''
Cannot make file {db_fname}.
You may need to make directory named {Path(db_fname).parent}.''')
        self.con = sqlite3.connect(fname)
        self.cur = self.con.cursor()
        self._make_new_tables()

    def _make_new_tables(self) -> None:
        if self._to_make_new:
            self.cur.execute('''CREATE TABLE tags
                             (id integer, tag text)''')
            self.cur.execute('''CREATE TABLE inode
                             (id integer, inode integer, color text)''')
        self.cur.execute('''INSERT INTO tags VALUES(0, NULL);''')
        self.need_to_make_new = False
        self.con.commit()

    def make_new_tag(self, tag: str) -> None:
        max_tag = list(self.cur.execute('''SELECT MAX(id) FROM tags;'''))[0][0]
        self.cur.execute('''INSERT INTO tags VALUES(?,?);''', (max_tag + 1, tag))
        self.con.commit()

    def _tag2id(self, tag: str) -> int:
        sql_iter = self.cur.execute('''SELECT id
                                    FROM tags
                                    WHERE tag = ?''', (tag,))
        result = list(sql_iter)
        if len(result) == 0:
            if logger.level == DEBUG:
                raise BaseException('No such tag.')
            else:
                stderr.write(f'No such tag: {tag}\n')
                self.__exit__()
                exit()
        return cast(int, result[0][0])

    def has_tag(self, inode: str, tag: str) -> bool:
        matched = list(self.cur.execute('''SELECT inode
                                      FROM inode
                                      JOIN tags
                                      ON inode.id = tags.id
                                      WHERE tag=?
                                        AND inode=?''', (tag, inode)))
        return True if len(matched) else False

    def add_tag(self, inode: str, tag: str, color: Optional[str]=None) -> None:
        if self.has_tag(inode, tag):
            return None
        self.cur.execute('''INSERT INTO inode VALUES(?,?,?);''',
                         (self._tag2id(tag), inode, color))
        self.con.commit()

    def __enter__(self) -> 'DB':
        return self

    def tag2inode(self, tag: int) -> List[str]:
        sql_iter = self.cur.execute('''SELECT inode
                               FROM tags
                               JOIN inode
                               ON tags.id = inode.id
                               WHERE tag = ?;''', (tag,))
        result = list(sql_iter)
        self.con.commit()
        return [r[0] for r in result]

    def show(self) -> None:
        print('tags', list(self.cur.execute('select * from tags')))
        print('inode', list(self.cur.execute('select * from inode')))

    def inode2tag(self, inode: str) -> List[str]:
        sql_iter = self.cur.execute('''SELECT tag
                               FROM tags
                               JOIN inode
                               ON tags.id = inode.id
                               WHERE inode = ?;''', (inode,))
        result = list(sql_iter)
        self.con.commit()
        return [r[0] for r in result]

    def __exit__(self, *arg: Any) -> None:
        self.con.close()

    def close(self) -> None:
        self.__exit__()

