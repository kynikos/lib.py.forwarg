import pytest
import shlex

from . import forwarg as _m_forwarg
import argparse as _m_argparse


def test1(parser):
    parser.add_argument('--0', dest='zero')
    assert parser.parse_args(shlex.split('--0 foo')).namespace == \
        _m_argparse.Namespace(zero='foo')

# TODO: Add more tests...
