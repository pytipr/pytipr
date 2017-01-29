# -*- coding: utf-8 -*-

import os
import pytest
import shutil

import tipr

@pytest.fixture
def datadir(tmpdir, request):
    '''
    Fixture responsible for searching a folder with the same name of test
    module and, if available, moving all contents to a temporary directory so
    tests can use them freely.
    '''
    filename = request.module.__file__
    test_dir, _ = os.path.splitext(filename)

    if os.path.isdir(test_dir):
        if os.path.exists(str(tmpdir)):
            shutil.rmtree(str(tmpdir))
        shutil.copytree(test_dir, str(tmpdir))

    return tmpdir

@pytest.mark.parametrize('act,exp', [
    ('Test 0\\', 'Test 0\\'),
    ('Foo\nbar', 'Foo\nbar'),
    ('Räksmörgås', 'Räksmörgås'),
    (
        '''Foo
        bar''',
        '''Foo
        bar'''),
])
# uses datadir fixture from above:
def test_file(datadir, act, exp):
    '''Write and read the same file, check content stays unchanged.'''
    filename = 'file_1.ini'
    filename_abs = datadir.join(filename)
    tipr.write_file(filename=filename_abs, text=act)
    with open(str(filename_abs), 'r') as f:
        content = f.read()
    assert content == exp
