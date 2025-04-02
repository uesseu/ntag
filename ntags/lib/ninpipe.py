#!usr/bin/env python3
from sys import stdin, stdout
from typing import List
from threading import Thread
from glob import glob


class Pipe:
    '''
    Class to use pipe.
    It is iterable and read lines by 'for statement'.
    Further more, it can read lines asynchronously.
    Asynchronous method is async_iter().
    '''

    def __init__(self, sep: str = '\n') -> None:
        '''
        sep: str
            Separator of each lines.
            It may be '\n' if libe based.
            Multiple characters cannot be contained.
        '''
        self.sep = sep
        self.ended = False

    def get_all_lines(self) -> List[str]:
        '''
        Get all the stdin.
        It is not good for performance.
        '''
        text = []
        while (True):
            try:
                text.append(input())
            except Exception:
                break
        return text

    def get(self, num: int = 0) -> str:
        '''
        Get one line stdin.

        num: int = 0
            Length of string to read.
            If it is 0, string will be read until 'sep' was read.
        '''
        if self.ended:
            raise EOFError
        if num != 0:
            return stdin.read(num)
        string: List[str] = []
        while True:
            data = stdin.read(1)
            if data == '':
                self.ended = True
                self.result = ''.join(string)
                return self.result
            elif data == self.sep:
                self.result = ''.join(string)
                return self.result
            else:
                string.append(data)

    def __next__(self) -> str:
        if self.ended:
            raise StopIteration
        result = self.get()
        if result == '':
            raise StopIteration
        return result

    def __iter__(self) -> 'Pipe':
        return self

    def async_iter(self) -> 'AsyncPipe':
        '''
        Asynchronous version.
        Because it cannot detect EOF asynchronously, you must detect EOF.
        If it is blank string, EOF was arrived.
        And so, EOF can be detected by code like below.

        >>> for data in Pipe().async_iter():
        >>>     received = data.receive()
        >>>     if not received:
        >>>         break
        '''
        return AsyncPipe(self)

    def put(self, data: str) -> None:
        '''
        Write data to stdout.
        '''
        stdout.write(data)


class PipeFname(Pipe):
    def __init__(self, sep: str = '\n',
                 from_glob: bool = False, directory: str = '') -> None:
        '''
        sep: str
            Separator of each lines.
            It may be '\n' if libe based.
            Multiple characters cannot be contained.
        directory: str
            Path of directory.
            If it is not blank string, the file list
            in the directory will be scanned and stdin
            will be ignored.
        '''
        self.sep = sep
        self.ended = False
        self.from_glob = from_glob
        self.directory = directory
        self.started = False
        self.fnum = 0

    def get(self, num: int = 0) -> str:
        '''
        Get one line stdin.

        num: int = 0
            Length of string to read.
            If it is 0, string will be read until 'sep' was read.
        '''
        if self.from_glob:
            if not self.started:
                self.glob_iter = iter(glob(self.directory))
                self.started = True
            try:
                self.result = next(self.glob_iter)
            except StopIteration:
                self.ended = True
                return ''
            return self.result
        if self.ended:
            raise EOFError
        if num != 0:
            return stdin.read(num)
        string: List[str] = []
        while True:
            data = stdin.read(1)
            if data == '':
                self.ended = True
                self.result = ''.join(string)
                return self.result
            elif data == self.sep:
                self.result = ''.join(string)
                return self.result
            else:
                string.append(data)


class AsyncPipe:
    '''
    Asynchronous version of Pipe class.
    It should be called by Pipe class.
    '''

    def __init__(self, pipe: Pipe) -> None:
        self.pipe = pipe

    def request(self, num: int = 0) -> 'AsyncPipe':
        self.reading = Thread(target=self.pipe.get, args=(num,))
        self.reading.start()
        self.now_reading = True
        return self

    def receive(self) -> str:
        if self.now_reading:
            self.reading.join()
        return self.pipe.result

    def __next__(self) -> 'AsyncPipe':
        if self.pipe.ended:
            raise StopIteration
        return self.request()

    def __iter__(self) -> 'AsyncPipe':
        return self


def main() -> None:
    for n in Pipe().async_iter():
        if not n.receive():
            break
        print(n.receive(),  'h')


if __name__ == '__main__':
    main()
