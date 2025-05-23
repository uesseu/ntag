from typing import Dict, cast
import platform
if platform.system() == 'Windows':
    from ctypes import windll, wintypes, byref
    handle = windll.kernel32.GetStdHandle(-11)
    windll.kernel32.SetConsoleMode(
        handle,
        windll.kernel32.GetConsoleMode(handle, byref(wintypes.DWORD()))
        | 0x0004
    )


prefix = '\033['
suffix = 'm'
win_prefix = '\x1b['

ATTRIBUTE: Dict[str, str] = dict(
    RESET='0',
    BOLD='1',
    DIMM='2',
    ITALIC='3',
    UNDERLINE='4',
    BLINK='5',
    FAST_BLINK='6',
    REVERCE2='7',
    INVISIBLE='8',
    MIDLINE='9',
    DOUBLE_LINE='21',
)

COLOR: Dict[str, str] = dict(
    BLACK='30',
    RED='31',
    GREEN='32',
    YELLOW='33',
    BLUE='34',
    MAGENTA='35',
    CYAN='36',
    WHITE='37',
    DEFAULT='39',
)

BG_COLOR: Dict[str, str] = dict(
    BLACK='40',
    RED='41',
    GREEN='42',
    YELLOW='43',
    BLUE='44',
    MAGENTA='45',
    CYAN='46',
    WHITE='47',
    DEFAULT='49',
)


def encode_color(attribute: str = 'RESET', color: str = 'DEFAULT',
                 bg_color: str = 'DEFAULT') -> str:
    body = ";".join((ATTRIBUTE[attribute], COLOR[color], BG_COLOR[bg_color]))
    return f'{prefix}{body}{suffix}'


def format_color(fname: str, color: str) -> str:
    if color is None:
        return fname
    return cast(str, color + fname + encode_color('RESET'))
