#!/usr/bin/env python
from ..lib.dbclass import DataBase, DEFAULT_TAGDB_FNAME, check_tagdb
from ..lib.color import COLOR, ATTRIBUTE, BG_COLOR, encode_color

def get_param(any_attr: dict) -> str:
    while True:
        attr = input()
        if attr.strip().upper() in any_attr.keys():
            return attr.strip().upper()

def main():
    print('Write tag name in this list')
    tag = input()
    print('Write one of the new attribute in this list.')
    print(' '.join(encode_color(attribute=key) + key + encode_color('RESET')
                   for key in ATTRIBUTE.keys()))
    attr = get_param(ATTRIBUTE)

    print('Write one of the new color in this list.')
    print(' '.join(encode_color(color=key) + key + encode_color('RESET')
          for key in COLOR.keys()))
    color = get_param(COLOR)

    print('Write one of the new background color in this list.')
    print(' '.join(encode_color(bg_color=key) + key + encode_color('RESET')
                   for key in BG_COLOR.keys()))
    bgcolor = get_param(COLOR)

    with DataBase(check_tagdb(DEFAULT_TAGDB_FNAME)) as db:
        db.set_color(tag, encode_color(attr, color, bgcolor))
