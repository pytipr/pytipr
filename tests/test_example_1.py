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
    infilename1 = str(tmpdir.join('input1.txt'))
    outfilename1 = str(tmpdir.join('output1.txt'))
    infilename2 = str(tmpdir.join('input2.txt'))
    outfilename2 = str(tmpdir.join('output2.txt'))
    with open(infilename1, 'w') as fobj:
        fobj.write(tipr_input)
    tipr.do(infilename1,  outfilename1)
    with open(outfilename1, 'r') as fobj:
        tipr_output_act = fobj.read()
    assert tipr_output_exp == tipr_output_act


def test_idempotency(tmpdir):
    '''Check that tipr.do() does the right thing two times in a row.'''
    infilename1 = str(tmpdir.join('input1.txt'))
    outfilename1 = str(tmpdir.join('output1.txt'))
    infilename2 = str(tmpdir.join('input2.txt'))
    outfilename2 = str(tmpdir.join('output2.txt'))
    with open(infilename1, 'w') as fobj:
        fobj.write(tipr_input)
    tipr.do(infilename1,  outfilename1)
    with open(outfilename1, 'r') as fobj:
        tipr_output_act = fobj.read()
    assert tipr_output_exp == tipr_output_act
    # repeat tipr.do() on output; must still be the same:
    with open(infilename2, 'w') as fobj:
        fobj.write(tipr_output_act)
    tipr.do(infilename2,  outfilename2)
    with open(outfilename2, 'r') as fobj:
        tipr_output_act = fobj.read()
    assert tipr_output_exp == tipr_output_act


tipr_input_case = '''
## user comment 1
user code 1
## tipr_Code_start
## tipr_result_IS="foo"
## tIpr_code_end
## tiPr_result_start
## Tipr_Result_End
## user comment 2
user code 2
'''


def test_case_insensitive_parsing(tmpdir):
    '''Check that tipr.do() does case-insensitive parsing of magic strings.'''
    infilename1 = str(tmpdir.join('input_1.txt'))
    outfilename1 = str(tmpdir.join('output_1.txt'))
    infilename2 = str(tmpdir.join('input_2.txt'))
    outfilename2 = str(tmpdir.join('output_2.txt'))
    with open(infilename1, 'w') as fobj:
        fobj.write(tipr_input_case)
    tipr.do(infilename1,  outfilename1)
    with open(outfilename1, 'r') as fobj:
        tipr_output_act = fobj.read()
    assert tipr_output_exp == tipr_output_act
