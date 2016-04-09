import pytest
import shlex

from . import forwarg as _m_forwarg
import argparse as _m_argparse


@pytest.fixture
def no_arguments(parser):
    return parser


@pytest.fixture
def _1_positional_argument(parser):
    parser.add_argument('pos1')
    return parser


@pytest.fixture
def _2_positional_arguments(parser):
    parser.add_argument('pos1')
    parser.add_argument('pos2')
    return parser


@pytest.fixture
def _1_optional_argument_long(parser):
    parser.add_argument('--opt1')
    return parser


@pytest.fixture
def _1_optional_argument_short(parser):
    parser.add_argument('-o')
    return parser


@pytest.fixture
def _1_optional_argument(parser):
    parser.add_argument('-o', '--opt1')
    return parser


@pytest.fixture
def _2_optional_arguments(parser):
    parser.add_argument('-o', '--opt1')
    parser.add_argument('-p', '--opt2')
    return parser


@pytest.fixture
def _2_mixed_arguments(parser):
    parser.add_argument('pos1')
    parser.add_argument('-o', '--opt1')
    return parser


NO_ARGS = ''
_1_POS_ARG = 'foo'
_2_POS_ARGS = 'foo bar'
_1_OPT_ARG = '--opt1 foo'
_2_OPT_ARGS = '--opt1 foo -pbar'


def parse(parser, case):
    return parser.parse_args(shlex.split(case)).namespace


def test_no_arguments_0(no_arguments):
    assert parse(no_arguments, NO_ARGS) == _m_argparse.Namespace()


def test_no_arguments_1p(no_arguments):
    with pytest.raises(_m_forwarg.UnknownArgumentError):
        parse(no_arguments, _1_POS_ARG)


def test_no_arguments_2p(no_arguments):
    with pytest.raises(_m_forwarg.UnknownArgumentError):
        parse(no_arguments, _2_POS_ARGS)


def test_no_arguments_1o(no_arguments):
    with pytest.raises(_m_forwarg.UnknownArgumentError):
        parse(no_arguments, _1_OPT_ARG)


def test_no_arguments_2o(no_arguments):
    with pytest.raises(_m_forwarg.UnknownArgumentError):
        parse(no_arguments, _2_OPT_ARGS)


def test_1_positional_0(_1_positional_argument):
    with pytest.raises(_m_forwarg.InsufficientArgumentsError):
        parse(_1_positional_argument, NO_ARGS)


def test_1_positional_1p(_1_positional_argument):
    assert parse(_1_positional_argument, _1_POS_ARG) == _m_argparse.Namespace(
                                                                    pos1='foo')


def test_1_positional_2p(_1_positional_argument):
    with pytest.raises(_m_forwarg.UnknownArgumentError):
        parse(_1_positional_argument, _2_POS_ARGS)


def test_1_positional_1o(_1_positional_argument):
    with pytest.raises(_m_forwarg.UnknownArgumentError):
        parse(_1_positional_argument, _1_OPT_ARG)


def test_1_positional_2o(_1_positional_argument):
    with pytest.raises(_m_forwarg.UnknownArgumentError):
        parse(_1_positional_argument, _2_OPT_ARGS)


def test_2_positional_0(_2_positional_arguments):
    with pytest.raises(_m_forwarg.InsufficientArgumentsError):
        parse(_2_positional_arguments, NO_ARGS)


def test_2_positional_1p(_2_positional_arguments):
    with pytest.raises(_m_forwarg.InsufficientArgumentsError):
        parse(_2_positional_arguments, _1_POS_ARG)


def test_2_positional_2p(_2_positional_arguments):
    assert parse(_2_positional_arguments, _2_POS_ARGS) == \
                                _m_argparse.Namespace(pos1='foo', pos2='bar')


def test_2_positional_1o(_2_positional_arguments):
    with pytest.raises(_m_forwarg.UnknownArgumentError):
        parse(_2_positional_arguments, _1_OPT_ARG)


def test_2_positional_2o(_2_positional_arguments):
    with pytest.raises(_m_forwarg.UnknownArgumentError):
        parse(_2_positional_arguments, _2_OPT_ARGS)


def test_1_optional_long_0(_1_optional_argument_long):
    assert parse(_1_optional_argument_long, NO_ARGS) == _m_argparse.Namespace(
                                                                    opt1=None)


def test_1_optional_long_1p(_1_optional_argument_long):
    with pytest.raises(_m_forwarg.UnknownArgumentError):
        parse(_1_optional_argument_long, _1_POS_ARG)


def test_1_optional_long_2p(_1_optional_argument_long):
    with pytest.raises(_m_forwarg.UnknownArgumentError):
        parse(_1_optional_argument_long, _2_POS_ARGS)


def test_1_optional_long_1o(_1_optional_argument_long):
    assert parse(_1_optional_argument_long, _1_OPT_ARG) == \
                                            _m_argparse.Namespace(opt1='foo')


def test_1_optional_long_2o(_1_optional_argument_long):
    with pytest.raises(_m_forwarg.UnknownArgumentError):
        parse(_1_optional_argument_long, _2_OPT_ARGS)


def test_1_optional_short_0(_1_optional_argument_short):
    assert parse(_1_optional_argument_short, NO_ARGS) == _m_argparse.Namespace(
                                                                        o=None)


def test_1_optional_short_1p(_1_optional_argument_short):
    with pytest.raises(_m_forwarg.UnknownArgumentError):
        parse(_1_optional_argument_short, _1_POS_ARG)


def test_1_optional_short_2p(_1_optional_argument_short):
    with pytest.raises(_m_forwarg.UnknownArgumentError):
        parse(_1_optional_argument_short, _2_POS_ARGS)


def test_1_optional_short_1o(_1_optional_argument_short):
    with pytest.raises(_m_forwarg.UnknownArgumentError):
        parse(_1_optional_argument_short, _1_OPT_ARG)


def test_1_optional_short_2o(_1_optional_argument_short):
    with pytest.raises(_m_forwarg.UnknownArgumentError):
        parse(_1_optional_argument_short, _2_OPT_ARGS)


def test_1_optional_0(_1_optional_argument):
    assert parse(_1_optional_argument, NO_ARGS) == _m_argparse.Namespace(
                                                                    opt1=None)


def test_1_optional_1p(_1_optional_argument):
    with pytest.raises(_m_forwarg.UnknownArgumentError):
        parse(_1_optional_argument, _1_POS_ARG)


def test_1_optional_2p(_1_optional_argument):
    with pytest.raises(_m_forwarg.UnknownArgumentError):
        parse(_1_optional_argument, _2_POS_ARGS)


def test_1_optional_1o(_1_optional_argument):
    assert parse(_1_optional_argument, _1_OPT_ARG) == _m_argparse.Namespace(
                                                                    opt1='foo')


def test_1_optional_2o(_1_optional_argument):
    with pytest.raises(_m_forwarg.UnknownArgumentError):
        parse(_1_optional_argument, _2_OPT_ARGS)


def test_2_optional_0(_2_optional_arguments):
    assert parse(_2_optional_arguments, NO_ARGS) == _m_argparse.Namespace(
                                                        opt1=None, opt2=None)


def test_2_optional_1p(_2_optional_arguments):
    with pytest.raises(_m_forwarg.UnknownArgumentError):
        parse(_2_optional_arguments, _1_POS_ARG)


def test_2_optional_2p(_2_optional_arguments):
    with pytest.raises(_m_forwarg.UnknownArgumentError):
        parse(_2_optional_arguments, _2_POS_ARGS)


def test_2_optional_1o(_2_optional_arguments):
    assert parse(_2_optional_arguments, _1_OPT_ARG) == _m_argparse.Namespace(
                                                        opt1='foo', opt2=None)


def test_2_optional_2o(_2_optional_arguments):
    assert parse(_2_optional_arguments, _2_OPT_ARGS) == _m_argparse.Namespace(
                                                        opt1='foo', opt2='bar')


def test_2_mixed_0(_2_mixed_arguments):
    with pytest.raises(_m_forwarg.InsufficientArgumentsError):
        parse(_2_mixed_arguments, NO_ARGS)


def test_2_mixed_1p(_2_mixed_arguments):
    assert parse(_2_mixed_arguments, _1_POS_ARG) == _m_argparse.Namespace(
                                                        pos1='foo', opt1=None)


def test_2_mixed_2p(_2_mixed_arguments):
    with pytest.raises(_m_forwarg.UnknownArgumentError):
        parse(_2_mixed_arguments, _2_POS_ARGS)


def test_2_mixed_1o(_2_mixed_arguments):
    with pytest.raises(_m_forwarg.InsufficientArgumentsError):
        parse(_2_mixed_arguments, _1_OPT_ARG)


def test_2_mixed_2o(_2_mixed_arguments):
    with pytest.raises(_m_forwarg.UnknownArgumentError):
        parse(_2_mixed_arguments, _2_OPT_ARGS)
