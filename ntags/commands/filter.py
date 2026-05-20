#!/usr/bin/env python
import sys
from datetime import datetime
from pathlib import Path
from argparse import ArgumentParser
from ..lib.dbclass import DataBase, DEFAULT_TAGDB_FNAME, Stat
from ..lib.color import format_color
from ..lib.misc import get_number_unit, set_custom_directory
from ..lib.ninpipe import PipeFname


def filter_command() -> None:
    parser = ArgumentParser(
        usage='''File name filter by tag.
If you are using pipe (not from tty), it reads filename from stdin.
If you are not using pipe (and from tty), it reads directory which
you set by option -d. If you did not set -d option, it reads
file names of files of current directory.
Multiple tag names can be set and this means 'or'.
If you want 'and', please run this command twice with pipe.

Options should be set after filter names.

Example.
ls ./*_good.csv | ntag filter good
ntag filter good -d ./

If you want to filter by file size or time, you can.
Size can be filtered by -u(--upper) and -l(--lower).
Time can be filtered by -T. Format of time is ISO 8601 format.
Additionally, you can write "now".

Example.
# A typical example. [from 2022/8/14 to 2023/2/11]
ntag filter good -T 2022-08-14/2023-02-11
# You can omit some string like "/" or same periods.
# [from 2025/2/09 to 2025/5/17]
ntag filter good -T 20220209/0517
# You can use special word "now" [from 2022/8/14 to now]
ntag filter good -T 20220814/now
''')
    parser.add_argument('command', help='Sub command.')
    parser.add_argument('tag', nargs='*', help='Tag name to show.')
    parser.add_argument('-v', '--invert', action='store_true',
                        help='Invert flag.')
    parser.add_argument('-c', '--comment', action='store_true',
                        help='With comment.')
    parser.add_argument('-f', '--fileonly', action='store_true',
                        help='Show files only.')
    parser.add_argument('-t', '--dironly', action='store_true',
                        help='Show directories only.')
    parser.add_argument('-B', '--byte-unit', default='',
                        help='Unit of the size of file.')
    parser.add_argument('-u', '--upper', default='', help='Max size of file.')
    parser.add_argument('-l', '--lower', default='',
                        help='Minimum size of file.')
    parser.add_argument('-T', '--time', default='/',
                        help='Get file newer than the date.'
                        'The grammer is based on ISO 8601 range format.'
                        '"/" must be included.'
                        )
    parser.add_argument('-m', '--timemode', default='c',
                        help='Time mode.'
                        'atime(access time),'
                        'mtime(modify time) and ctime(create time).'
                        'It can be 1 character like "a", "m", "c".'
                        )
    parser.add_argument('--parent', action='store_true')
    set_custom_directory(parser)
    args = parser.parse_args()
    upper = get_number_unit(args.upper)
    lower = get_number_unit(args.lower)
    if args.time:
        try:
            pre, post_tmp = (n.strip() for n in args.time.split('/'))
            post = pre[:len(pre) - len(post_tmp)]
            post += post_tmp
        except:
            raise Exception('Time must divided by "/" like "20220209/0517"')
        pre = datetime.now() if pre == 'now' else datetime.fromisoformat(pre)
        post = datetime.now() if post == 'now' else datetime.fromisoformat(post)
    mode = args.timemode[0].lower()

    with DataBase(
        DEFAULT_TAGDB_FNAME, args.directory if args.relative else ''
    ) as db:
        fnames = PipeFname(
            from_glob=sys.stdin.isatty() or args.directory is not None,
            directory=args.directory if args.directory else '.'
        ).async_iter()
        for data in fnames:
            fname = data.receive()
            if not fname:
                break
            path = Path(fname).absolute()
            if not path.exists():
                continue
            if args.dironly and not path.is_dir():
                continue
            if args.fileonly and not path.is_file():
                continue
            stat = Stat(fname)
            if args.upper:
                if stat.size > upper.as_byte:
                    continue
            if args.lower:
                if stat.size < lower.as_byte:
                    continue
            if args.time:
                if (datetime.fromtimestamp(stat.time[mode]) < pre
                     or datetime.fromtimestamp(stat.time[mode]) > post):
                    continue
            if args.tag:
                if not args.invert ^ db.has_tags(stat.inode, args.tag):
                    continue
            sys.stdout.write(fname)
            if sys.stdout.isatty():
                ftags = [
                    format_color(*tag) for tag in
                    db.inode2tag(stat.inode)
                ]
                sys.stdout.write(' [ ')
                sys.stdout.write(' '.join(ftags))
                sys.stdout.write(' ]')
            if args.comment:
                comment = db.get_comment(stat.inode)
                if comment:
                    sys.stdout.write(': ')
                    sys.stdout.write(comment[0])
            sys.stdout.write('\n')
