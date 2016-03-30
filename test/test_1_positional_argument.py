import pytest
import shlex

from . import forwarg as _m_forwarg
import argparse as _m_argparse


def parse(parser):
    return parser.parse_args(shlex.split('foo'))


def test_1_positional(_1_positional_argument):
    for parser in _1_positional_argument:
        assert parse(parser) == _m_argparse.Namespace(pos1='foo')


def test_2_positional(_2_positional_arguments):
    for parser in _2_positional_arguments:
        with pytest.raises(_m_forwarg.InsufficientArgumentsError):
            parse(parser)
