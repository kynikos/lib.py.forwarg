import pytest
import shlex

from . import forwarg as _m_forwarg
import argparse as _m_argparse


def parse(parser):
    return parser.parse_args(shlex.split('--opt1 foo -pbar'))


def test_no_arguments(no_arguments):
    for parser in no_arguments:
        with pytest.raises(_m_forwarg.UnknownArgumentError):
            parse(parser)


def test_1_positional(_1_positional_argument):
    for parser in _1_positional_argument:
        with pytest.raises(_m_forwarg.UnknownArgumentError):
            parse(parser)


def test_2_positional(_2_positional_arguments):
    for parser in _2_positional_arguments:
        with pytest.raises(_m_forwarg.UnknownArgumentError):
            parse(parser)


def test_1_optional_long(_1_optional_argument_long):
    for parser in _1_optional_argument_long:
        with pytest.raises(_m_forwarg.UnknownArgumentError):
            parse(parser)


def test_1_optional_short(_1_optional_argument_short):
    for parser in _1_optional_argument_short:
        with pytest.raises(_m_forwarg.UnknownArgumentError):
            parse(parser)


def test_1_optional(_1_optional_argument):
    for parser in _1_optional_argument:
        with pytest.raises(_m_forwarg.UnknownArgumentError):
            parse(parser)


def test_2_optional(_2_optional_arguments):
    for parser in _2_optional_arguments:
        assert parse(parser) == _m_argparse.Namespace(opt1='foo', opt2='bar')


def test_2_mixed(_2_mixed_arguments):
    for parser in _2_mixed_arguments:
        with pytest.raises(_m_forwarg.UnknownArgumentError):
            parse(parser)
