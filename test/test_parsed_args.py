import pytest
import shlex

from . import forwarg as _m_forwarg
import argparse as _m_argparse


def test1():
    parser = _m_forwarg.ArgumentParser()
    parser.add_argument('--foo')
    parser.parse_args(shlex.split('--foo bar'))
    assert parser.parsed_args == ['--foo', 'bar']

# TODO: Add more tests...
