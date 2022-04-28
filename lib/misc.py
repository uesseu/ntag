from argparse import ArgumentParser
from typing import cast

def get_tag_from_arg(example: str) -> str:
    parser = ArgumentParser()
    parser.add_argument('tag')
    args = parser.parse_args()
    if 'tag' not in args:
        print('Write tag name like this.')
        print(example)
        exit()
    return cast(str, args.tag)
