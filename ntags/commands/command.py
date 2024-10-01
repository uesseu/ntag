import sys
import typing
import os
from .add import add_command
from .color import color_command
from .delete import delete_command
from .filter import filter_command
from .init import init_command
from .list import list_command
from .make import make_command
from .remove import remove_command
from .show import show_command
from .status import status_command

commands = {}
commands['add'] = add_command
commands['color'] = color_command
commands['delete'] = delete_command
commands['filter'] = filter_command
commands['init'] = init_command
commands['list'] = list_command
commands['make'] = make_command
commands['remove'] = remove_command
commands['show'] = show_command
commands['status'] = status_command


def main():
    if len(sys.argv) > 1 and sys.argv[1] in commands.keys():
        commands[sys.argv[1]](from_root=True)
    else:
        print(f'''Tag maker for unix like system.
Please look subcommands for details.
This is list of subcommands.
{'\n'.join(commands.keys())}''')
