#!/usr/bin/env python

from setuptools import setup

VERSION = '1.0.0'
setup(
    name='ntfschattr',
    version=VERSION,
    description='A Python command-line utility for manipulating NTFS file attributes.',
    author='Giuliano Mega',
    author_email='giuliano.mega@gmail.com',
    license='BSD',
    packages=['ntfschattr'],
    entry_points={
        'console_scripts': [
            'ntfs-chattr = ntfschattr.cli:main'
        ]
    },
    python_requires=">=3.0",
    install_requires=['pyxattr']
)


