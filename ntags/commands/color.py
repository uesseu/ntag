#!/usr/bin/env python
from ..lib.dbclass import DataBase, DEFAULT_TAGDB_FNAME, check_tagdb
from ..lib.color import COLOR, ATTRIBUTE, BG_COLOR, encode_color, format_color

def input_int(num_range) -> int:
    while True:
        try:
            result = int(input('> '))
            if result < num_range:
                return result
            else:
                print(f'Please write number less than {num_range}')
        except Exception:
            print('Please write number')


def color_command(from_root: bool = False) -> None:
    print('Write tag number in this list')
    with DataBase(check_tagdb(DEFAULT_TAGDB_FNAME)) as db:
        taglist = list(db.get_taglist())
        for num, (tagname, color) in enumerate(taglist):
            if tagname is not None:
                print(num, format_color(tagname, color))
    tag_number = input_int(len(taglist))
    print('Write one of the new attribute number in this list.')
    attr_keys = list(ATTRIBUTE.keys())
    print(
        ' '.join(
            f"{num}: {encode_color(attribute=key)}{key}{encode_color('RESET')}"
            for num, key in enumerate(attr_keys)
        )
    )
    attr_num = input_int(len(attr_keys))
    color_list = list(COLOR.keys())
    print('Write one of the new color number in this list.')
    print(
        ' '.join(
            f"{num}: {encode_color(color=key)}{key}{encode_color('RESET')}"
            for num, key in enumerate(color_list))
    )
    color_num = input_int(len(color_list))
    bgcolor_list = list(BG_COLOR.keys())
    print('Write one of the new background color number in this list.')
    print(' '.join(
        f"{num}: {encode_color(bg_color=key)}{key}{encode_color('RESET')}"
        for num, key in enumerate(bgcolor_list))
          )
    bgcolor_num = input_int(len(bgcolor_list))
    with DataBase(check_tagdb(DEFAULT_TAGDB_FNAME)) as db:
        db.set_color(
            taglist[tag_number][0],
            encode_color(
                attr_keys[attr_num],
                color_list[color_num],
                bgcolor_list[bgcolor_num]
            )
        )
