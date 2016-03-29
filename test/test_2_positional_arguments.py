import pytest
import shlex

from . import forwarg as _m_forwarg
import argparse as _m_argparse


def parse(parser):
    return parser.parse_args(shlex.split('foo bar'))


def test_1_positional(_1_positional_argument):
    for parser in _1_positional_argument:
        with pytest.raises(_m_forwarg.UnknownArgumentError):
            parse(parser)


def test_2_positional(_2_positional_arguments):
    for parser in _2_positional_arguments:
        assert parse(parser) == {'pos1': 'foo',
                                 'pos2': 'bar'}
