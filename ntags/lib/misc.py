from argparse import ArgumentParser
import sys
from typing import cast
from datetime import datetime


class Command:
    help = ''
    def __init__(self):
        pass

    def run(self):
        pass


def get_tag_from_arg(usage: str, from_root=False) -> str:
    parser = ArgumentParser(usage=usage)
    if from_root:
        parser.add_argument('command')
    parser.add_argument('tag')
    args = parser.parse_args()
    if 'tag' not in args:
        print('Write tag name like this.')
        sys.exit()
    return cast(str, args.tag)


class ByteUnit:
    def __init__(self, number: int, unit: str):
        self.number = number
        self.unit = unit
        self.byte_order = self.get_byte_order()
        self.as_byte = number * self.byte_order

    def unit_is(self, texts: list[str]):
        unit = self.unit.strip().lower()
        for text in texts:
            if text.strip().lower() == unit:
                return True
        return False

    def get_byte_order(self):
        if self.unit_is(['', 'byte', 'b']):
            return 1
        if self.unit_is(
                ['kb', 'k', 'kilobyte', 'kilobytes', 'kbyte', 'kbytes']
        ):
            return 1024
        if self.unit_is(
                ['mb', 'm', 'megabyte', 'megabytes', 'mbyte', 'mbytes']
        ):
            return 1024 ** 2
        if self.unit_is(
                ['gb', 'g', 'gigabyte', 'gigabytes', 'gbyte', 'gbytes']
        ):
            return 1024 ** 3
        return 0


def get_number_unit(text: str) -> ByteUnit:
    number = ''
    unit = ''
    number_mode = True
    nums = [str(i) for i in range(10)] + ['.']
    for t in text:
        if number_mode:
            if t in nums:
                number += t
            else:
                number_mode = False
                unit += t
        else:
            unit += t
    return ByteUnit(0 if number == '' else float(number), unit)


def set_custom_directory(parser):
    parser.add_argument(
        '-d', '--directory', default=None,
        help='Directory path to read.'
        ' This option prevents readlines from stdin.'
    )
    parser.add_argument(
        '-r', '--relative', action='store_true',
        help='Load database from the relative path of "-d" option.'
    )


class TimeUnit:
    def __init__(self):
        self.days = 0
        self.seconds = 0
        self.milliseconds = 0

    def add(self, value: int, unit: str, is_date: bool):
        if unit.upper() == 'Y':
            if is_date:
                Exception(f'Value must be date "{value} {unit}"')
            self.days += value * 365
        elif unit.upper() == 'M':
            if is_date:
                self.days += value * 30
            else:
                self.seconds += value * 60
        elif unit.upper() == 'W':
            if is_date:
                Exception(f'Value must be date "{value} {unit}"')
            self.days += value * 7
        elif unit.upper() == 'D':
            if is_date:
                Exception(f'Value must be date "{value} {unit}"')
            self.days += value
        elif unit.upper() == 'H':
            if is_date:
                Exception(f'Value must be time "{value} {unit}"')
            self.seconds += value * 3600
        elif unit.upper() == 'S':
            if is_date:
                Exception(f'Value must be time "{value} {unit}"')
            self.seconds += value

    def __repr__(self):
        return f'{self.days} {self.seconds} {self.milliseconds}'

class TimedeltaParser:
    TITLE = 'PT'
    SEPS = 'PYMDTHS'

    def __init__(self, text):
        self.text = text
        self.length = len(text)
        self.cursor = 0
        self.is_date = True
        # self.date = 
        # self.date = dict(
        #     days=0,
        #     seconds=0,
        #     microseconds=0,
        #     milliseconds=0,
        #     minutes=0,
        #     hours=0,
        #     weeks=0
        # )

    def __next__(self) -> dict:
        if self.cursor == self.length:
            raise StopIteration
        if self.text[self.cursor] in self.TITLE:
            result = self.text[self.cursor]
            self.cursor += 1
            if result == 'T':
                self.is_date = False
            return dict(value=0, unit=result[-1], is_date=self.is_date)
        first_cursor = self.cursor
        while self.cursor != self.length\
                and self.text[self.cursor] not in self.SEPS:
            self.cursor += 1
        self.cursor += 1
        result = self.text[first_cursor: self.cursor]
        return dict(
            value=int(result[0:-1]),
            unit=result[-1],
            is_date=self.is_date
        )

    def __iter__(self):
        return self

    def to_timedelta(self):
        timeunit = TimeUnit()
        for n in self:
            timeunit.add(**n)
        return datetime.timedelta(
            timeunit.days,
            timeunit.seconds,
            timeunit.milliseconds
        )
