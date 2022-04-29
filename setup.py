from setuptools import setup, find_packages
import sys

if sys.version_info[:2] < (3, 7):
    raise RuntimeError("Python version >= 3.7 required.")


with open('README.md') as f:
    readme = f.read()

with open('LICENSE') as f:
    license = f.read()

VERSION = '0.0.1'

setup(
    name='ntags',
    version=VERSION,
    description='It adds file tags for any unix like systems.',
    long_description=readme,
    author='ninja',
    author_email='sheepwing@kyudai.jp',
    url='',
    license=license,
    package_dir={"ntags": "ntags"},
    packages=find_packages(
        where="ntags",
        exclude=('commands')
    ),
    entry_points={
        "console_scripts": [
            "ntag_color=ntags.commands.color:main",
            "ntag_delete=ntags.commands.delete:main",
            "ntag_init=ntags.commands.init:main",
            "ntag_list=ntags.commands.list:main",
            "ntag_make=ntags.commands.make:main",
            "ntag_show=ntags.commands.show:main",
            "ntag_add=ntags.commands.add:main",
            "ntag_remove=ntags.commands.remove:main",
            "ntag_rename=ntags.commands.rename:main",
            "ntag_status=ntags.commands.status:main"
        ]
    },
    python_requires='>=3.7'
)
