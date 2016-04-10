import pytest
import shlex

from . import forwarg as _m_forwarg
import argparse as _m_argparse


def test1():
    parser = _m_forwarg.ArgumentParser()
    argdef = parser.add_argument('--foo')
    parsedargs = parser.parse_args(shlex.split('--foo bar'))
    argholder = parsedargs.argdef_to_argholder[argdef]
    assert parsedargs.splitline[0].arg == '--foo'
    assert parsedargs.splitline[0].argholder == argholder
    assert parsedargs.splitline[1].arg == 'bar'
    assert parsedargs.splitline[1].argholder == argholder


def test2():
    parser = _m_forwarg.ArgumentParser()
    argdef = parser.add_argument('--foo')
    parsedargs = parser.parse_args(shlex.split('--foo=bar'))
    argholder = parsedargs.argdef_to_argholder[argdef]
    assert parsedargs.splitline[0].arg == '--foo=bar'
    assert parsedargs.splitline[0].argholder == argholder


def test3():
    parser = _m_forwarg.ArgumentParser()
    argdef = parser.add_argument('-o')
    parsedargs = parser.parse_args(shlex.split('-o=bar'))
    argholder = parsedargs.argdef_to_argholder[argdef]
    assert parsedargs.splitline[0].prefix == '-'
    assert parsedargs.splitline[0].options[0].subindex == 0
    assert parsedargs.splitline[0].options[0].string == 'o=bar'
    assert parsedargs.splitline[0].options[0].argholder == argholder

# TODO: Add more tests...
