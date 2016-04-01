import pytest
import shlex

from . import forwarg as _m_forwarg
import argparse as _m_argparse


def parse(parser):
    return parser.parse_args([])


def test_no_arguments(no_arguments):
    for parser in no_arguments:
        assert parse(parser) == _m_argparse.Namespace()


def test_1_positional(_1_positional_argument):
    for parser in _1_positional_argument:
        with pytest.raises(_m_forwarg.InsufficientArgumentsError):
            parse(parser)


def test_2_positional(_2_positional_arguments):
    for parser in _2_positional_arguments:
        with pytest.raises(_m_forwarg.InsufficientArgumentsError):
            parse(parser)


def test_1_optional_long(_1_optional_argument_long):
    for parser in _1_optional_argument_long:
        assert parse(parser) == _m_argparse.Namespace(opt1=None)


def test_1_optional_short(_1_optional_argument_short):
    for parser in _1_optional_argument_short:
        assert parse(parser) == _m_argparse.Namespace(o=None)


def test_1_optional(_1_optional_argument):
    for parser in _1_optional_argument:
        assert parse(parser) == _m_argparse.Namespace(opt1=None)


def test_2_optional(_2_optional_arguments):
    for parser in _2_optional_arguments:
        assert parse(parser) == _m_argparse.Namespace(opt1=None, opt2=None)


def test_2_mixed(_2_mixed_arguments):
    for parser in _2_mixed_arguments:
        with pytest.raises(_m_forwarg.InsufficientArgumentsError):
            parse(parser)
