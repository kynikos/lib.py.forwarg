import pytest
import shlex

from . import forwarg as _m_forwarg
import argparse as _m_argparse


def test1():
    parser = _m_forwarg.ArgumentParser()
    foo = parser.add_argument('--foo')
    parsedargs = parser.parse_args(shlex.split('--foo bar'))
    fooholder = parsedargs.argdef_to_argholder[foo]
    assert parsedargs.splitline == [('--foo', fooholder), ('bar', fooholder)]

# TODO: Add more tests...
