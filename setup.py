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
    author='Shoichiro Nakanishi',
    author_email='sheepwing@kyudai.jp',
    url='',
    license=license,
    entry_points={
        "console_scripts": [
            "ntag-color=ntags.commands.color:main",
            "ntag-delete=ntags.commands.delete:main",
            "ntag-init=ntags.commands.init:main",
            "ntag-list=ntags.commands.list:main",
            "ntag-make=ntags.commands.make:main",
            "ntag-show=ntags.commands.show:main",
            "ntag-add=ntags.commands.add:main",
            "ntag-remove=ntags.commands.remove:main",
            "ntag-rename=ntags.commands.rename:main",
            "ntag-filter=ntags.commands.filter:main",
            "ntag-status=ntags.commands.status:main"
        ]
    },
    python_requires='>=3.7'
)
