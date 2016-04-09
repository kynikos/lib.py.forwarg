import pytest
import shlex

from . import forwarg as _m_forwarg
import argparse as _m_argparse


def test1(parser):
    parser.add_argument('-O', action='store_true')
    parser.add_argument('-P')
    assert parser.parse_args(shlex.split('-OP foo')).namespace == \
        _m_argparse.Namespace(O=True, P='foo')

# TODO: Add more tests...
