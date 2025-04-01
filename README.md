# ntags
A python package to enable tag style command line file management.
Written for my daily life.

# Why?
Because I wanted such CLI tools Like "FenrirFS".
But I could not find such tools. That is all.

# Feature

- Made by python and sqlite3.
- Tag does not removed even if file is moved.
- Not so light weighted, because of python.
  + But has enough speed for daily life.
- Written for "me".
- Color is only for unix like system now.
  + If I or you want color in windows, it may be developped.
- Add comment for files.

# Install

```
pip install git+https://github.com/uesseu/ntag
```

# Usage
Please read help text in the command.

```
ntag -h
```

```
ntag add -h
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
