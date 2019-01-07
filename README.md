# ntfs-chattr

manipulate NTFS attributes from the command line using GNU/Linux

## Overview
`ntfs-chattr` is a simple command-line utility which allows you to manipulate NTFS attributes from the command line. In 
particular, you can add/remove all of the supported 
[extended NTFS attributes](https://www.tuxera.com/community/ntfs-3g-advanced/extended-attributes/#ntfsattributes) such
as `system`, `hidden`, or `readonly`.

`ntfs-chattr` is based on [pyxattr](https://pyxattr.k1024.org/). 


## Installation
The simplest way is to just install the master tarball via `pip`:

```{bash}
pip install https://github.com/django-extensions/django-extensions/zipball/master
```

## Usage Examples

### Adding/Removing Attributes
Remove attributes `system` and `hidden` from file `/foo/bar.txt`:

```
ntfs-chattr modify /foo/bar.txt --remove system hidden
```

Add attributes `system` and `hidden` from file `/foo/bar.txt`:

```
ntfs-chattr modify /foo/bar.txt --add system hidden
```

Recursively add attributes `system` and `hidden` to folder `/foo` and all of its subfolders and files:
```
ntfs-chattr modify /foo --add system hidden --recursive --verbose
```

### Listing Valid NTFS Attributes

See the list of recognized NTFS attributes which can be added/removed:
```{bash}
$ ntfs-chattr list --valid

Valid NTFS attributes are:
- content_not_indexed
- readonly
- temporary
- compressed
- offline
- hidden
- system
- archive
```

### Listing the Attributes of a Given File
See which attributes are set for a given file:

```{bash}
$ ntfs-chattr list --file '/foo/bar.txt'            
/foo/bar.txt: [hidden,system]
```

