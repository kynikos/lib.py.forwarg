import pytest
import shlex

from . import forwarg as _m_forwarg
import argparse as _m_argparse


def test1():
    parser = _m_forwarg.ArgumentParser()
    foo = parser.add_argument('--foo')
    assert parser.parse_args(shlex.split('--foo bar')
                             ).parsed == [('--foo', foo), ('bar', foo)]

# TODO: Add more tests...
