# -*- coding: utf-8 -*-

'''pytipr, the Python Template In-Place Replacer.'''

from __future__ import print_function

def write_file(filename, text='Hello world!'):
    '''Write a simple file.'''
    with open(str(filename), 'w') as fobj:
        fobj.write(text)


def do(infilename, outfilename):
    '''Read infilename, do transformation, write outfilename.'''
    with open(infilename, 'r') as rfobj, open(outfilename, 'w') as wfobj:
        for line in rfobj:
            if line.startswith('## tipr_'):  # hey, something interesting
                if line.startswith('## tipr_result_is'):
                    wfobj.write(line)  # repeat in output
                    code = line[len('## '):]
                    print('code={0}'.format(code))
                    exec(code)  # tipr_result_is will be filled now
                    print('tipr_result_is={0}'.format(tipr_result_is))
                if line.startswith('## tipr_result_start'):
                    wfobj.write(line)  # repeat in output
                    wfobj.write(tipr_result_is)  # write the result
                if line.startswith('## tipr_result_end'):
                    wfobj.write(line)  # repeat in output
                # tipr_code_start and tipr_code_end:
                if line.startswith('## tipr_code'):
                    wfobj.write(line)  # repeat in output
            else:
                wfobj.write(line)  # nothing interesting, pass through
