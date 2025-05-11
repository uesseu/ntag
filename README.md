# ntags
A small python package to enable tag style command line file management.
Written for my daily life.

# Why?
Because I wanted such CLI tools like itunes or FenrirFS for file management.
But I could not find such tools. That is all.

# Feature

- Made by python and sqlite3.
- Multi-platform.
  + Linux(tested)
  + Windows(tested)
  + May be MacOS and android(Not tested)
- Tag does not removed even if file is renamed or moved.
- Not so light weighted, because of python.
  + But has enough speed for daily life.
- Colored tag.
- Filter and sort command.
- Add comment for files.
- Written for "me".


I am a heavy user of ntag and this is the only fact which may give it reliability. If you are a heavy user of some software, you must require reliability, dont you? ;-)

# Requirements

- python upper than 3.8
- sqlite3
- Terminal emulator, which can display color
  + Linux and windows terminal could display it

# Install

```
pip install git+https://github.com/uesseu/ntag
```

For bash users, it offers bash completion.
Please download below.

```
https://github.com/uesseu/ntag/ntag_complete.sh
```

You can copy the content and paset into the bashrc.
But I recommend you to source the file, because I may edit the script someday.

```sh
source ntag_complete.sh
```

# Usage
Please read the help text in the command.

```
ntag -h
```

```
ntag add -h
```

# Example

```sh
# Initialize tag database in the directory.
ntag init

# Make tag named 'red'. It must be piped.
echo red | ntag make

# Set 'red' tag to all the jpg files.
ls *.jpg | ntag make

# Interactive color configuration
ntag color

# Filter the file.
ntag filter red

# Add comment
echo hentai.jpg | ntag add_comment 'Not for child!'
```

# Command list
## Manage tags

- init   : Initialize tag database
- make   : Make a tag
- color  : Set color of tag
- delete : Delete tag
- status : Show current status

## Use tags

- add    : Add tag
- filter : Filter by tag
- list   : Show list of all the tag
- remove : Remove tag from file
- show   : Show files with tag
- sort   : Sort result of ntag
- path   : Add or remove strings on result

## Use comments

- add_comment : Add comment to file
- get_comment : Get comment from file
- filter_comment : Filter files by comment

# Name of database
It makes a sqlite3 database in the directory. The default database name is '.nintag_db'. If you want to change the filename, edit environmental variable, named 'NINTAG_DB' and you can use other filename.

# Do not rewrite inode
This software manages database of inode(unix like system) or file index(windows).
And so, if you rewrite them, it lose the path. Users should configure editors if the editor rewrite inode in default configuration.

In case of vim, please write below in vimrc.

```vim
set backupcopy=yes
```

Unfortunate , I do not know about emacs or vscode.

# Compatibility issue
Mac OS and android and iOS was not tested, because I have no Mac, no iphone and no ipad. If someone use it in such machines, please report me. I can not pay money but must appreciate a lot!

# Licence
Mit.
