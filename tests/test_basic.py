# -*- coding: utf-8 -*-

'''Basic tests.'''

from mako.template import Template
from mako.lookup import TemplateLookup

import os
import pytest
import shutil

import tipr


# pylint: disable=W0621
@pytest.fixture
def datadir(tmpdir, request):
    '''
    Fixture responsible for searching a folder with the same name of test
    module and, if available, moving all contents to a temporary directory so
    tests can use them freely.
    From http://stackoverflow.com/a/29631801
    '''
    filename = request.module.__file__
    test_dir, _ = os.path.splitext(filename)

    if os.path.isdir(test_dir):
        if os.path.exists(str(tmpdir)):
            shutil.rmtree(str(tmpdir))
        shutil.copytree(test_dir, str(tmpdir))

    return tmpdir


@pytest.mark.parametrize('act, exp', [
    ('Test 0\\', 'Test 0\\'),
    ('Foo\nbar', 'Foo\nbar'),
    ('Räksmörgås', 'Räksmörgås'),
    (
        '''Foo
        bar''',
        '''Foo
        bar'''),
])
def test_file(tmpdir, act, exp):
    '''Write and read the same file, check content stays unchanged.'''
    filename = 'file_1.ini'
    filename_abs = str(tmpdir.join(filename))
    tipr.write_file(filename=filename_abs, text=act)
    with open(filename_abs, 'r') as fobj:
        content = fobj.read()
    assert content == exp


def test_mako(tmpdir):
    '''Generate a mako template, render it to file, check file is correct.'''
    tmplfilename = str(tmpdir.join('template.mako'))
    outfilename = str(tmpdir.join('out.txt'))
    with open(tmplfilename, 'w') as fobj:
        fobj.write('hello ${word}')
    tobj = Template(filename=tmplfilename, module_directory='.')
    with open(outfilename, 'w') as fobj:
        fobj.write(tobj.render(word='world'))
    with open(outfilename, 'r') as fobj:
        content = fobj.read()
    assert content == 'hello world'


@pytest.mark.parametrize('tmpl, word, exp', [
    ('hello ${word}', 'world', 'hello world'),
    ('${word}\n${word}', 'foo', 'foo\nfoo'),
])
def test_mako2(tmpdir, tmpl, word, exp):
    '''Generate a mako template, render it to file, check file is correct.'''
    tmplfilename = str(tmpdir.join('template.mako'))
    outfilename = str(tmpdir.join('out.txt'))
    with open(tmplfilename, 'w') as fobj:
        fobj.write(tmpl)
    tobj = Template(filename=tmplfilename, module_directory='.')
    with open(outfilename, 'w') as fobj:
        fobj.write(tobj.render(word=word))
    with open(outfilename, 'r') as fobj:
        content = fobj.read()
    assert content == exp
