import sqlite3
from typing import List, cast, Any, Optional, Union, Tuple, Iterable
from os.path import exists
from logging import getLogger, INFO, DEBUG
from pathlib import Path
import sys
from os import stat, environ
from stat import ST_INO
logger = getLogger()
logger.setLevel(INFO)
DEFAULT_TAGDB_FNAME = '.nintag_db'


def find_tagdb_inparents(fname: str) -> Optional[Path]:
    '''Returns file name of database in parent directories.
    If there is no database file, returns None.'''
    current_dir_filepath = Path('.') / fname
    if current_dir_filepath.exists():
        return current_dir_filepath
    for path in Path('.').absolute().parents:
        dbpath = path / fname
        if dbpath.exists():
            return dbpath
    return fname


def check_tagdb(fname: str) -> str:
    '''
    Find tag file and returns the name.
    It kills this program itself if there is no tag file.
    '''
    db_fname: Union[Path, str, None] = None
    if 'NINTAG_DB' in environ:
        db_fname = environ['NINTAG_DB']
    else:
        db_fname = find_tagdb_inparents(fname)
    if db_fname is None:
        print('Database is not made yet.')
        print('Consider "ntag init" to make it in current directory.')
        sys.exit()
    return str(db_fname)


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


class DataBase:
    def __init__(self, fname: str):
        self.db_fname = check_tagdb(fname)
        self._to_make_new: bool = False if exists(fname) else True
        if not Path(self.db_fname).parent.exists():
            raise FileNotFoundError(
                f'''Cannot make file {self.db_fname}.
You may need to make directory named {Path(self.db_fname).parent}.''')
        self.con = sqlite3.connect(fname)
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

    def remove_tag_from_inode(self, tag: str, inode: int) -> None:
        tid = self._tag2id(tag)
        self.cur.execute(
            '''DELETE from inode WHERE id=? AND inode=?;''',
            (tid, inode)
        )
        self.con.commit()

    def delete_tag(self, tag: str) -> None:
        tid = self._tag2id(tag)
        self.cur.execute(
            '''DELETE from inode WHERE id=?;''',
            (tid,)
        )
        self.cur.execute(
            '''DELETE from tags WHERE id=?''',
            (tid,)
        )
        self.con.commit()

    def rename_tag(self, tag: str, name: str) -> None:
        self.cur.execute(
            '''UPDATE tags SET tag=? WHERE tag=?;''',
            (name, tag)
        )
        self.con.commit()

    def _tag2id(self, tag: str) -> int:
        sql_iter = self.cur.execute(
            '''SELECT id FROM tags
            WHERE tag = ?''',
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

    def has_tag(self, inode: int, tag: str) -> bool:
        matched = list(self.cur.execute(
            '''SELECT inode
            FROM inode JOIN tags ON inode.id = tags.id
            WHERE tag=? AND inode=?''',
            (tag, inode)))
        return True if len(matched) else False

    def has_tags(self, inode: int, tags: List[str]) -> bool:
        return any(self.has_tag(inode, tag) for tag in tags)

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
            (self._tag2id(tag), inode)
        )
        self.con.commit()

    def __enter__(self) -> 'DataBase':
        return self

    def tag2inode(self, tag: int) -> List[str]:
        sql_iter = self.cur.execute(
            '''SELECT inode
            FROM tags JOIN inode ON tags.id = inode.id
            WHERE tag = ?;''',
            (tag,)
        )
        result = list(sql_iter)
        self.con.commit()
        return [r[0] for r in result]

    def show(self) -> None:
        print('tags', list(self.cur.execute('select * from tags')))
        print('inode', list(self.cur.execute('select * from inode')))

    def get_taglist(self) -> Iterable[Tuple[str, str]]:
        return self.cur.execute('select tag, color from tags')

    def inode2tag(self, inode: int) -> List[str]:
        sql_iter = self.cur.execute(
            '''SELECT tag, color
            FROM tags JOIN inode ON tags.id = inode.id
            WHERE inode = ?;''',
            (inode,)
        )
        result = list(sql_iter)
        self.con.commit()
        return [r for r in result]

    def __exit__(self, *arg: Any) -> None:
        self.con.close()

    def close(self) -> None:
        self.__exit__()


def print_status(db: DataBase) -> None:
    if 'NINTAG_DB' in environ:
        print('NINTAG_DB:',
              environ['NINTAG_DB'],
              '\n  Environment of NINTAG_DB')
    print('Path of current database:', Path(db.db_fname).absolute())
