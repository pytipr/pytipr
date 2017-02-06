# -*- coding: utf-8 -*-

'''pytipr, the Python Template In-Place Replacer.'''

# FIXME: __init__.py should be empty and this code in another file

from __future__ import print_function

import logging


def write_file(filename, text='Hello world!'):
    '''Write a simple file.'''

    write_file_log = logging.getLogger('tipr.write_file')
    write_file_log.debug('write_file function called')

    with open(str(filename), 'w') as fobj:
        fobj.write(text)


def do(infilename, outfilename):
    '''Read infilename, do transformation, write outfilename.'''
    namespace = {}
    with open(infilename, 'r') as rfobj, open(outfilename, 'w') as wfobj:
        for line in rfobj:
            # FIXME: we need to keep track of parsing state here
            if line.lower().startswith('## tipr_'):  # hey, something interesting
                if line.lower().startswith('## tipr_result_is'):
                    wfobj.write(line)  # repeat in output
                    code = line[len('## '):]
                    exec(code, namespace)  # namespace needed in Python 3
                    namespace_lower = {k.lower():v for k,v in namespace.items()}
                    tipr_result_is = namespace_lower['tipr_result_is']
                if line.lower().startswith('## tipr_result_start'):
                    wfobj.write(line)  # repeat in output
                    wfobj.write(tipr_result_is+'\n')  # write the result
                if line.lower().startswith('## tipr_result_end'):
                    wfobj.write(line)  # repeat in output
                # tipr_code_start and tipr_code_end:
                if line.lower().startswith('## tipr_code'):
                    wfobj.write(line)  # repeat in output
            else:
                wfobj.write(line)  # nothing interesting, pass through
