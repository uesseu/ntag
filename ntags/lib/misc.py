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
