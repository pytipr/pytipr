# -*- coding: utf-8 -*-

'''pytipr, the Python Template In-Place Replacer.'''

from __future__ import print_function

import logging


def write_file(filename, text='Hello world!'):
    '''Write a simple file.'''

    write_file_log = logging.getLogger('tipr.write_file')
    write_file_log.debug('write_file function called')

    with open(str(filename), 'w') as fobj:
        fobj.write(text)


# FIXME: use better state machine, like
#        https://python-3-patterns-idioms-test.readthedocs.io/en/latest/StateMachine.html
def do(infilename, outfilename):
    '''Read infilename, do transformation, write outfilename.'''
    namespace = {}
    with open(infilename, 'r') as rfobj, open(outfilename, 'w') as wfobj:
        state = "idle"
        state_with_error = ""
        for line in rfobj:
            if line.lower().startswith('## tipr_'):  # hey, something interesting
                if line.lower().startswith('## tipr_code_start'):
                    state = "code_start"
                    wfobj.write(line)  # repeat in output
                if line.lower().startswith('## tipr_result_is'):
                    if state != "code_start":
                        state_with_error = "result_is, got {0}".format(state)
                    state = "result_is"
                    wfobj.write(line)  # repeat in output
                    code = line[len('## '):]
                    exec(code, namespace)  # namespace needed in Python 3
                    namespace_lower = {k.lower():v for k,v in namespace.items()}
                    tipr_result_is = namespace_lower['tipr_result_is']
                if line.lower().startswith('## tipr_code_end'):
                    if state != "result_is":
                        state_with_error = "result_is, got {0}".format(state)
                    wfobj.write(line)  # repeat in output
                if line.lower().startswith('## tipr_result_start'):
                    if state != "result_is":
                        state_with_error = "result_start, got {0}".format(state)
                    state = "result_start"
                    wfobj.write(line)  # repeat *this* line in output
                    # ... but not any other lines until we hit tipr_result_end
                if line.lower().startswith('## tipr_result_end'):
                    if state != "result_start":
                        state_with_error = "result_end, got {0}".format(state)
                    state = "idle"  # state machine is through
                    wfobj.write(tipr_result_is+'\n')  # write the result
                    wfobj.write(line)  # repeat in output
            else:
                if state != "result_start":
                    wfobj.write(line)  # nothing interesting, pass through
        if state_with_error != "":
            logging.error("Parser noticed an error in state {0}!".format(state_with_error))
