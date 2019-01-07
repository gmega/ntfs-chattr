import os
from argparse import ArgumentParser

from ntfschattr.ntfsutils import NtfsFile, NTFS_ATTRIBUTE_TABLE


def main():
    parser = ArgumentParser()
    subparsers = parser.add_subparsers()
    subparsers.required = True
    subparsers.dest = 'command'

    list_parser = subparsers.add_parser('list', help='lists NTFS attributes')
    grp = list_parser.add_mutually_exclusive_group(required=True)
    grp.add_argument('file', help='lists the NTFS attributes of given file', nargs='?')
    grp.add_argument('--valid', help='lists valid NTFS attributes', action='store_true')
    list_parser.set_defaults(func=list_attributes)

    modify_parser = subparsers.add_parser('modify', help='modifies NTFS attributes')
    modify_parser.add_argument('file', help='file to change attributes')
    modify_parser.add_argument('-e', '--recursive', help='if the target file is a folder, recursively '
                                                         'applies the modification to all subfiles and folders',
                               action='store_true')
    modify_parser.add_argument('-v', '--verbose', help='verbose mode', action='store_true')
    modify_parser.add_argument('-a', '--add', choices=list(NTFS_ATTRIBUTE_TABLE.keys()), nargs='+',
                               default=[], metavar='attribute,')
    modify_parser.add_argument('-r', '--remove', choices=list(NTFS_ATTRIBUTE_TABLE.keys()), nargs='+',
                               default=[], metavar='attribute,')
    modify_parser.set_defaults(func=do_modify)

    args = parser.parse_args()

    try:
        args.func(args)
    except FileNotFoundError:
        print('%s: not found' % args.file)


def do_modify(args):
    modify_path(args.file, args)


def modify_path(path, args):
    if args.recursive and os.path.isdir(path):
        for subpath in os.listdir(path):
            subpath = os.path.join(path, subpath)
            if args.verbose:
                print('Recursing into %s' % subpath)
            modify_path(subpath, args)
    modify_file(path, args)


def modify_file(path, args):
    if args.verbose:
        print('Modifying %s' % path)
    a = NtfsFile(path)
    for attribute in args.add:
        a.set_attribute(attribute)
    for attribute in args.remove:
        a.clear_attribute(attribute)


def list_attributes(args):
    if args.valid:
        list_valid_attributes()
    else:
        list_file_attributes(args.file)


def list_valid_attributes():
    print('Valid NTFS attributes are:')
    for attribute in NTFS_ATTRIBUTE_TABLE.keys():
        print('- %s' % attribute)


def list_file_attributes(target):
    print(NtfsFile(target))
