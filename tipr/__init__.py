# -*- coding: utf-8 -*-

'''pytipr, the Python Template In-Place Replacer.'''

from __future__ import print_function

def write_file(filename, text='Hello world!'):
    with open(str(filename), 'w') as f:
        f.write(text)
