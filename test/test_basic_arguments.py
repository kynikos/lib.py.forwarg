import pytest
import shlex

from . import forwarg as _m_forwarg
import argparse as _m_argparse


@pytest.fixture
def no_arguments(parsers):
    for parser in parsers:
        parser.add_argument_group('group1', 'description1')

    return parsers


@pytest.fixture
def _1_positional_argument(parsers):
    for parser in parsers:
        group1 = parser.add_argument_group('group1', 'description1')
        group1.add_argument('pos1')

    return parsers


@pytest.fixture
def _2_positional_arguments(parsers):
    for parser in parsers:
        group1 = parser.add_argument_group('group1', 'description1')
        group1.add_argument('pos1')
        group1.add_argument('pos2')

    return parsers


@pytest.fixture
def _1_optional_argument_long(parsers):
    for parser in parsers:
        group1 = parser.add_argument_group('group1', 'description1')
        group1.add_argument('--opt1')

    return parsers


@pytest.fixture
def _1_optional_argument_short(parsers):
    for parser in parsers:
        group1 = parser.add_argument_group('group1', 'description1')
        group1.add_argument('-o')

    return parsers


@pytest.fixture
def _1_optional_argument(parsers):
    for parser in parsers:
        group1 = parser.add_argument_group('group1', 'description1')
        group1.add_argument('-o', '--opt1')

    return parsers


@pytest.fixture
def _2_optional_arguments(parsers):
    for parser in parsers:
        group1 = parser.add_argument_group('group1', 'description1')
        group1.add_argument('-o', '--opt1')
        group1.add_argument('-p', '--opt2')

    return parsers


@pytest.fixture
def _2_mixed_arguments(parsers):
    for parser in parsers:
        group1 = parser.add_argument_group('group1', 'description1')
        group1.add_argument('pos1')
        group1.add_argument('-o', '--opt1')

    return parsers


NO_ARGS = ''
_1_POS_ARG = 'foo'
_2_POS_ARGS = 'foo bar'
_1_OPT_ARG = '--opt1 foo'
_2_OPT_ARGS = '--opt1 foo -pbar'


def parse(parser, case):
    return parser.parse_args(shlex.split(case))


def test_no_arguments_0(no_arguments):
    for parser in no_arguments:
        assert parse(parser, NO_ARGS) == _m_argparse.Namespace()


def test_no_arguments_1p(no_arguments):
    for parser in no_arguments:
        with pytest.raises(_m_forwarg.UnknownArgumentError):
            parse(parser, _1_POS_ARG)


def test_no_arguments_2p(no_arguments):
    for parser in no_arguments:
        with pytest.raises(_m_forwarg.UnknownArgumentError):
            parse(parser, _2_POS_ARGS)


def test_no_arguments_1o(no_arguments):
    for parser in no_arguments:
        with pytest.raises(_m_forwarg.UnknownArgumentError):
            parse(parser, _1_OPT_ARG)


def test_no_arguments_2o(no_arguments):
    for parser in no_arguments:
        with pytest.raises(_m_forwarg.UnknownArgumentError):
            parse(parser, _2_OPT_ARGS)


def test_1_positional_0(_1_positional_argument):
    for parser in _1_positional_argument:
        with pytest.raises(_m_forwarg.InsufficientArgumentsError):
            parse(parser, NO_ARGS)


def test_1_positional_1p(_1_positional_argument):
    for parser in _1_positional_argument:
        assert parse(parser, _1_POS_ARG) == _m_argparse.Namespace(pos1='foo')


def test_1_positional_2p(_1_positional_argument):
    for parser in _1_positional_argument:
        with pytest.raises(_m_forwarg.UnknownArgumentError):
            parse(parser, _2_POS_ARGS)


def test_1_positional_1o(_1_positional_argument):
    for parser in _1_positional_argument:
        with pytest.raises(_m_forwarg.UnknownArgumentError):
            parse(parser, _1_OPT_ARG)


def test_1_positional_2o(_1_positional_argument):
    for parser in _1_positional_argument:
        with pytest.raises(_m_forwarg.UnknownArgumentError):
            parse(parser, _2_OPT_ARGS)


def test_2_positional_0(_2_positional_arguments):
    for parser in _2_positional_arguments:
        with pytest.raises(_m_forwarg.InsufficientArgumentsError):
            parse(parser, NO_ARGS)


def test_2_positional_1p(_2_positional_arguments):
    for parser in _2_positional_arguments:
        with pytest.raises(_m_forwarg.InsufficientArgumentsError):
            parse(parser, _1_POS_ARG)


def test_2_positional_2p(_2_positional_arguments):
    for parser in _2_positional_arguments:
        assert parse(parser, _2_POS_ARGS) == _m_argparse.Namespace(pos1='foo',
                                                                   pos2='bar')


def test_2_positional_1o(_2_positional_arguments):
    for parser in _2_positional_arguments:
        with pytest.raises(_m_forwarg.UnknownArgumentError):
            parse(parser, _1_OPT_ARG)


def test_2_positional_2o(_2_positional_arguments):
    for parser in _2_positional_arguments:
        with pytest.raises(_m_forwarg.UnknownArgumentError):
            parse(parser, _2_OPT_ARGS)


def test_1_optional_long_0(_1_optional_argument_long):
    for parser in _1_optional_argument_long:
        assert parse(parser, NO_ARGS) == _m_argparse.Namespace(opt1=None)


def test_1_optional_long_1p(_1_optional_argument_long):
    for parser in _1_optional_argument_long:
        with pytest.raises(_m_forwarg.UnknownArgumentError):
            parse(parser, _1_POS_ARG)


def test_1_optional_long_2p(_1_optional_argument_long):
    for parser in _1_optional_argument_long:
        with pytest.raises(_m_forwarg.UnknownArgumentError):
            parse(parser, _2_POS_ARGS)


def test_1_optional_long_1o(_1_optional_argument_long):
    for parser in _1_optional_argument_long:
        assert parse(parser, _1_OPT_ARG) == _m_argparse.Namespace(opt1='foo')


def test_1_optional_long_2o(_1_optional_argument_long):
    for parser in _1_optional_argument_long:
        with pytest.raises(_m_forwarg.UnknownArgumentError):
            parse(parser, _2_OPT_ARGS)


def test_1_optional_short_0(_1_optional_argument_short):
    for parser in _1_optional_argument_short:
        assert parse(parser, NO_ARGS) == _m_argparse.Namespace(o=None)


def test_1_optional_short_1p(_1_optional_argument_short):
    for parser in _1_optional_argument_short:
        with pytest.raises(_m_forwarg.UnknownArgumentError):
            parse(parser, _1_POS_ARG)


def test_1_optional_short_2p(_1_optional_argument_short):
    for parser in _1_optional_argument_short:
        with pytest.raises(_m_forwarg.UnknownArgumentError):
            parse(parser, _2_POS_ARGS)


def test_1_optional_short_1o(_1_optional_argument_short):
    for parser in _1_optional_argument_short:
        with pytest.raises(_m_forwarg.UnknownArgumentError):
            parse(parser, _1_OPT_ARG)


def test_1_optional_short_2o(_1_optional_argument_short):
    for parser in _1_optional_argument_short:
        with pytest.raises(_m_forwarg.UnknownArgumentError):
            parse(parser, _2_OPT_ARGS)


def test_1_optional_0(_1_optional_argument):
    for parser in _1_optional_argument:
        assert parse(parser, NO_ARGS) == _m_argparse.Namespace(opt1=None)


def test_1_optional_1p(_1_optional_argument):
    for parser in _1_optional_argument:
        with pytest.raises(_m_forwarg.UnknownArgumentError):
            parse(parser, _1_POS_ARG)


def test_1_optional_2p(_1_optional_argument):
    for parser in _1_optional_argument:
        with pytest.raises(_m_forwarg.UnknownArgumentError):
            parse(parser, _2_POS_ARGS)


def test_1_optional_1o(_1_optional_argument):
    for parser in _1_optional_argument:
        assert parse(parser, _1_OPT_ARG) == _m_argparse.Namespace(opt1='foo')


def test_1_optional_2o(_1_optional_argument):
    for parser in _1_optional_argument:
        with pytest.raises(_m_forwarg.UnknownArgumentError):
            parse(parser, _2_OPT_ARGS)


def test_2_optional_0(_2_optional_arguments):
    for parser in _2_optional_arguments:
        assert parse(parser, NO_ARGS) == _m_argparse.Namespace(opt1=None,
                                                               opt2=None)


def test_2_optional_1p(_2_optional_arguments):
    for parser in _2_optional_arguments:
        with pytest.raises(_m_forwarg.UnknownArgumentError):
            parse(parser, _1_POS_ARG)


def test_2_optional_2p(_2_optional_arguments):
    for parser in _2_optional_arguments:
        with pytest.raises(_m_forwarg.UnknownArgumentError):
            parse(parser, _2_POS_ARGS)


def test_2_optional_1o(_2_optional_arguments):
    for parser in _2_optional_arguments:
        assert parse(parser, _1_OPT_ARG) == _m_argparse.Namespace(opt1='foo',
                                                                  opt2=None)


def test_2_optional_2o(_2_optional_arguments):
    for parser in _2_optional_arguments:
        assert parse(parser, _2_OPT_ARGS) == _m_argparse.Namespace(opt1='foo',
                                                                   opt2='bar')


def test_2_mixed_0(_2_mixed_arguments):
    for parser in _2_mixed_arguments:
        with pytest.raises(_m_forwarg.InsufficientArgumentsError):
            parse(parser, NO_ARGS)


def test_2_mixed_1p(_2_mixed_arguments):
    for parser in _2_mixed_arguments:
        assert parse(parser, _1_POS_ARG) == _m_argparse.Namespace(pos1='foo',
                                                                  opt1=None)


def test_2_mixed_2p(_2_mixed_arguments):
    for parser in _2_mixed_arguments:
        with pytest.raises(_m_forwarg.UnknownArgumentError):
            parse(parser, _2_POS_ARGS)


def test_2_mixed_1o(_2_mixed_arguments):
    for parser in _2_mixed_arguments:
        with pytest.raises(_m_forwarg.InsufficientArgumentsError):
            parse(parser, _1_OPT_ARG)


def test_2_mixed_2o(_2_mixed_arguments):
    for parser in _2_mixed_arguments:
        with pytest.raises(_m_forwarg.UnknownArgumentError):
            parse(parser, _2_OPT_ARGS)
