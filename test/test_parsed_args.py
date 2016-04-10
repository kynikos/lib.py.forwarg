import pytest
import shlex

from . import forwarg as _m_forwarg
import argparse as _m_argparse


def test1():
    parser = _m_forwarg.ArgumentParser()
    argdef = parser.add_argument('--foo')
    parsedargs = parser.parse_args(shlex.split('--foo bar'))
    argholder = parsedargs.argdef_to_argholder[argdef]
    assert parsedargs.splitline == [('--foo', argholder), ('bar', argholder)]
    assert argholder.parsed_arg_indices == [0, 1]


def test2():
    parser = _m_forwarg.ArgumentParser()
    argdef = parser.add_argument('--foo')
    parsedargs = parser.parse_args(shlex.split('--foo=bar'))
    argholder = parsedargs.argdef_to_argholder[argdef]
    assert parsedargs.splitline == [('--foo=bar', argholder)]
    assert argholder.parsed_arg_indices == [0]


def test3():
    parser = _m_forwarg.ArgumentParser()
    argdef = parser.add_argument('-o')
    parsedargs = parser.parse_args(shlex.split('-o=bar'))
    argholder = parsedargs.argdef_to_argholder[argdef]
    assert parsedargs.splitline == [[('-', None), ('o=bar', argholder)]]
    assert argholder.parsed_arg_indices == [(0, 1)]

# TODO: Add more tests...
