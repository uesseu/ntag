import sqlite3
from typing import List, cast, Any, Optional, Union, Tuple, Iterable
from os.path import exists
from logging import getLogger, INFO, DEBUG
from pathlib import Path
from .defaults import DEFAULT_TAGDB_FNAME, DEFAULT_TAGJSON_FNAME
import sys
import shutil
from os import stat, environ
from stat import (
    ST_INO, ST_GID, ST_SIZE, ST_CTIME, ST_MTIME,
    ST_ATIME, ST_NLINK, ST_MODE, ST_DEV, ST_UID
)
logger = getLogger()
logger.setLevel(INFO)


def find_tagdb_inparents(fname: str, directory: str | None = None) -> Optional[Path]:
    '''Returns file name of database in parent directories.
    If there is no database file, returns None.'''
    filepath = Path(directory if directory else '.') / fname
    if filepath.exists():
        return filepath
    for path in filepath.absolute().parents:
        dbpath = path / fname
        if dbpath.exists():
            return dbpath.absolute()
    return None



def check_tagdb(fname: str, directory: str | None = None) -> str:
    '''
    Find tag file and returns the name.
    It kills this program itself if there is no tag file.
    '''
    fname = environ['NINTAG_DB'] if 'NINTAG_DB' in environ else fname
    db_fname: Path | None = find_tagdb_inparents(fname, directory)
    if db_fname is None:
        print('Database is not made yet.')
        print('Consider "ntag init" to make it in current directory.')
        sys.exit()
    return str(db_fname)


def check_tagjson(fname: str, directory: str | None = None) -> str:
    '''
    Find tag file and returns the name.
    It kills this program itself if there is no tag file.
    '''
    fname = environ['NINTAG_JSON'] if 'NINTAG_JSON' in environ else fname
    db = find_tagdb_inparents(fname, directory)
    if db:
        return db.parent / DEFAULT_TAGJSON_FNAME


class Stat:
    def __init__(self, fname):
        self.fname = fname
        self.inode = 0
        self.size = 0
        self.uid = None
        self.gid = None
        self.time = {}
        self.load()

    def load(self):
        if exists(self.fname):
            self.stat = stat(Path(self.fname).absolute())
            self.inode = self.stat[ST_INO]
            self.size = self.stat[ST_SIZE]
            self.uid = self.stat[ST_UID]
            self.gid = self.stat[ST_GID]
            self.time = {
                'c': self.stat[ST_CTIME],
                'a': self.stat[ST_ATIME],
                'm': self.stat[ST_MTIME]
            }


def get_inode(fname: str) -> Optional[int]:
    if exists(fname):
        return stat(Path(fname).absolute())[ST_INO]


def get_all(fname: str) -> int:
    return stat(Path(fname).absolute())


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


class DataBaseBase:
    def __init__(self, fname: str, directory: str | None = None,
                 make_new: bool = False):
        self.db_fname = check_tagdb(fname, directory)
        shutil.copy(self.db_fname, self.db_fname + '_backup')
        self._to_make_new: bool = make_new and not exists(self.db_fname)
        if not Path(self.db_fname).parent.exists():
            raise FileNotFoundError(
                f'''Cannot make file {self.db_fname}.
You may need to make directory named {Path(self.db_fname).parent}.''')
        if not Path(self.db_fname).exists():
            print('No database')
            sys.exit()
        self.con = sqlite3.connect(self.db_fname)
        self.cur = self.con.cursor()
        self._make_new_tables()

    def _make_new_tables(self) -> None:
        if self._to_make_new:
            self.cur.execute(
                '''CREATE TABLE tags (id integer, tag text, color text)'''
            )
            self.cur.execute(
                '''CREATE TABLE inode (id integer, inode integer)'''
            )
            self.cur.execute(
                '''CREATE TABLE comment (inode integer, comment text)'''
            )
        self.need_to_make_new = False
        self.con.commit()

    def __enter__(self) -> 'DataBase':
        return self

    def __exit__(self, *arg: Any) -> None:
        self.con.close()

    def close(self) -> None:
        self.__exit__()


class TagDataBase(DataBaseBase):
    def make_new_tag(self, tag: str, color: Optional[str] = None) -> None:
        if len(list(self.cur.execute(
            '''SELECT tag FROM tags WHERE tag==?;''',
                (tag,)))):
            return None
        max_tag = next(
            self.cur.execute('''SELECT MAX(id) FROM tags;''')
        )[0]
        if not max_tag:
            max_tag = 0
        self.cur.execute(
            '''INSERT INTO tags (id, tag, color) VALUES(?,?,?);''',
            (max_tag + 1, tag, color)
        )
        self.con.commit()

    def set_color(self, tag: str, color: Optional[str] = None) -> None:
        self.cur.execute(
            '''UPDATE tags SET color=? WHERE tag=?;''',
            (color, tag)
        )
        self.con.commit()

    def rename_tag(self, tag: str, name: str) -> None:
        self.cur.execute(
            '''UPDATE tags SET tag=? WHERE tag=?;''',
            (name, tag)
        )
        self.con.commit()

    def tag2id(self, tag: str) -> int:
        sql_iter = self.cur.execute(
            '''SELECT id FROM tags WHERE tag = ?''',
            (tag,)
        )
        result = list(sql_iter)
        if len(result) == 0:
            if logger.level == DEBUG:
                raise BaseException('No such tag.')
            else:
                sys.stderr.write(f'No such tag: {tag}\n')
                self.__exit__()
                sys.exit()
        return cast(int, result[0][0])


class DataBase(TagDataBase):

    def remove_tag_from_inode(self, tag: str, inode: int) -> None:
        tid = self.tag2id(tag)
        self.cur.execute(
            '''DELETE from inode WHERE id=? AND inode=?;''',
            (tid, inode)
        )
        self.con.commit()

    def delete_tag(self, tag: str) -> None:
        tid = self.tag2id(tag)
        self.cur.execute(
            '''DELETE from inode WHERE id=?;''',
            (tid,)
        )
        self.cur.execute(
            '''DELETE from tags WHERE id=?''',
            (tid,)
        )
        self.con.commit()

    def has_tag(self, inode: int, tag: str) -> bool:
        matched = (self.cur.execute(
            '''SELECT inode, tag
            FROM inode JOIN tags ON inode.id = tags.id
            WHERE tag=? AND inode=?''',
            (tag, inode)))
        return any(matched)

    def add_comment(self, inode: int, comment: str):
        if self.get_comment(inode):
            self.cur.execute(
                '''UPDATE comment SET comment=? WHERE inode=?;''',
                (comment, inode)
            )
        else:
            self.cur.execute(
                '''INSERT INTO comment (inode, comment) VALUES(?,?);''',
                (inode, comment)
            )
        self.con.commit()

    def get_comment(self, inode: int) -> tuple[str]:
        inodes = list(self.cur.execute(
            '''SELECT comment FROM comment WHERE inode=?''',
            (inode,)
        ))
        return inodes[0] if inodes else None

    def add_tag(self, inode: int, tag: str) -> None:
        if self.has_tag(inode, tag):
            return None
        self.cur.execute(
            '''INSERT INTO inode (id, inode) VALUES(?,?);''',
            (self.tag2id(tag), inode)
        )
        self.con.commit()

    def show(self) -> None:
        print('tags', list(self.cur.execute('select * from tags')))
        print('inode', list(self.cur.execute('select * from inode')))

    def get_taglist(self) -> Iterable[Tuple[str, str]]:
        return self.cur.execute('select tag, color from tags')

    def path2tag(self, path: str) -> list[tuple[str]]:
        """
        Return tag and color of path, not using inode.
        """
        sql_iter = self.cur.execute(
            '''SELECT tag, color
            FROM tags JOIN inode ON tags.id = path.id
            WHERE path = ?;''',
            (Path(path).resolve(),)
        )
        return self.cur.fetchall()

    def inode2tag(self, inode: int) -> list[tuple[str]]:
        """
        Return tag and color of inode.
        """
        sql_iter = self.cur.execute(
            '''SELECT tag, color
            FROM tags JOIN inode ON tags.id = inode.id
            WHERE inode = ?;''',
            (inode,)
        )
        return self.cur.fetchall()

    def get_color(self, tag):
        sql_iter = self.cur.execute(
            '''SELECT color FROM tags WHERE tag = ?;''',
            (tag,)
        )
        return self.cur.fetchall()[0][0]


def print_status(db: DataBase) -> None:
    if 'NINTAG_DB' in environ:
        print('NINTAG_DB:',
              environ['NINTAG_DB'],
              '\n  Environment of NINTAG_DB')
    print('Path of current database:', Path(db.db_fname).absolute())
