from setuptools import setup, find_packages
import sys

if sys.version_info[:2] < (3, 7):
    raise RuntimeError("Python version >= 3.7 required.")


with open('README.md') as f:
    readme = f.read()

with open('LICENSE') as f:
    license = f.read()

VERSION = '0.0.2'

setup(
    name='ntags',
    version=VERSION,
    description='It adds file tags for any unix like systems.',
    long_description=readme,
    author='Shoichiro Nakanishi',
    author_email='sheepwing@kyudai.jp',
    url='',
    license=license,
    entry_points={
        "console_scripts": [
            "ntag-color=ntags.commands.color:color_command",
            "ntag-delete=ntags.commands.delete:delete_command",
            "ntag-init=ntags.commands.init:init_command",
            "ntag-list=ntags.commands.list:list_command",
            "ntag-make=ntags.commands.make:make_command",
            "ntag-show=ntags.commands.show:show_command",
            "ntag-add=ntags.commands.add:add_command",
            "ntag-remove=ntags.commands.remove:remove_command",
            "ntag-rename=ntags.commands.rename:rename_command",
            "ntag-filter=ntags.commands.filter:filter_command",
            "ntag-status=ntags.commands.status:status_command",
            "ntag=ntags.commands.command:main"
        ]
    },
    python_requires='>=3.7'
)
