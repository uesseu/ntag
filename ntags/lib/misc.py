from argparse import ArgumentParser
import sys
from typing import cast


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
        if self.unit_is(['kb', 'k', 'kilobyte', 'kbyte']):
            return 1024
        if self.unit_is(['mb', 'm', 'megabyte', 'mbyte']):
            return 1024 ** 2
        if self.unit_is(['gb', 'g', 'gigabyte', 'gbyte']):
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
