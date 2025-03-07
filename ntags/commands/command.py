import sys
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
from .io import export_command, import_command
from .comment import addcomment_command
from .comment import getcomment_command
from .sort import sort_command
from .path import path_command
from .cleanup import cleanup_command

commands = {}
commands['export'] = export_command
commands['import'] = import_command
commands['add'] = add_command
commands['color'] = color_command
commands['delete'] = delete_command
commands['filter'] = filter_command
commands['init'] = init_command
commands['list'] = list_command
commands['make'] = make_command
commands['remove'] = remove_command
commands['show'] = show_command
commands['path'] = path_command
commands['sort'] = sort_command
commands['status'] = status_command
commands['add_comment'] = addcomment_command
commands['get_comment'] = getcomment_command
commands['cleanup'] = cleanup_command


def main():
    if len(sys.argv) > 1 and sys.argv[1] in commands.keys():
        commands[sys.argv[1]]()
    else:
        print('''Tag maker for unix like system.
Please look subcommands for details.
This is list of subcommands.

# Manage tags
init    : Initialize tag database
make    : Make a tag
color   : Set color of tag
delete  : Delete tag
status  : Show current status
cleanup : Clean up unused tags

# Use tags
add    : Add tag
filter : Filter by tag
list   : Show list of all the tag
remove : Remove tag from file
show   : Show files with tag
sort   : Sort result of ntag
path   : Add or remove strings on result

# Use comments
add_comment : Add comment to file
get_comment : Get comment from file
''')
