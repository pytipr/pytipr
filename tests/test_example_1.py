# -*- coding: utf-8 -*-

'''Tests with real tipr examples.'''

from mako.template import Template
from mako.lookup import TemplateLookup

import os
import pytest
import shutil

import tipr


# pylint: disable=W0621
tipr_input = '''
## user comment 1
user code 1
## tipr_code_start
## tipr_result_is="foo"
## tipr_code_end
## tipr_result_start
## tipr_result_end
## user comment 2
user code 2
'''

tipr_output_exp = '''
## user comment 1
user code 1
## tipr_code_start
## tipr_result_is="foo"
## tipr_code_end
## tipr_result_start
foo
## tipr_result_end
## user comment 2
user code 2
'''

def test_example_1(tmpdir):
    '''Check that tipr.do() does the right thing with a well-behaved example.'''
    infilename = str(tmpdir.join('input.txt'))
    outfilename = str(tmpdir.join('output.txt'))
    with open(infilename, 'w') as fobj:
        fobj.write(tipr_input)
    tipr.do(infilename,  outfilename)
    with open(outfilename, 'r') as fobj:
        tipr_output_act = fobj.read()
    assert tipr_output_exp == tipr_output_act
    # FIXME: repeat tipr.do() on outfilename; must still be the same
