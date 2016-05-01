import pytest
import shlex

from . import forwarg as _m_forwarg
import argparse as _m_argparse


# TODO: Compare all the results with argparse (they must behave the same)
#@pytest.fixture(params = [_m_argparse, _m_forwarg])
@pytest.fixture(params=[_m_forwarg])
def parser_dash(request):
    parser = request.param.ArgumentParser()
    parser.add_argument('-f', '--foo', action='store_true')
    return parser


def test_dash_single_1(parser_dash):
    with pytest.raises(_m_forwarg.UnknownArgumentError):
        parser_dash.parse_args(shlex.split('-'))


def test_dash_single_2(parser_dash):
    with pytest.raises(_m_forwarg.UnknownArgumentError):
        parser_dash.parse_args(shlex.split('- --foo'))


def test_dash_single_3(parser_dash):
    with pytest.raises(_m_forwarg.UnknownArgumentError):
        parser_dash.parse_args(shlex.split('--foo -'))


def test_dash_single_4(parser_dash):
    with pytest.raises(_m_forwarg.UnknownArgumentError):
        parser_dash.parse_args(shlex.split('-f - --foo'))


# The double-dash cases are tested in test_double_dash.py


def test_dash_triple_1(parser_dash):
    with pytest.raises(_m_forwarg.UnknownArgumentError):
        parser_dash.parse_args(shlex.split('---'))


def test_dash_triple_2(parser_dash):
    with pytest.raises(_m_forwarg.UnknownArgumentError):
        parser_dash.parse_args(shlex.split('--- --foo'))


def test_dash_triple_3(parser_dash):
    with pytest.raises(_m_forwarg.UnknownArgumentError):
        parser_dash.parse_args(shlex.split('--foo ---'))


def test_dash_triple_4(parser_dash):
    with pytest.raises(_m_forwarg.UnknownArgumentError):
        parser_dash.parse_args(shlex.split('-f --- --foo'))


def test_dash_quadruple_1(parser_dash):
    with pytest.raises(_m_forwarg.UnknownArgumentError):
        parser_dash.parse_args(shlex.split('----'))


def test_dash_quadruple_2(parser_dash):
    with pytest.raises(_m_forwarg.UnknownArgumentError):
        parser_dash.parse_args(shlex.split('---- --foo'))


def test_dash_quadruple_3(parser_dash):
    with pytest.raises(_m_forwarg.UnknownArgumentError):
        parser_dash.parse_args(shlex.split('--foo ----'))


def test_dash_quadruple_4(parser_dash):
    with pytest.raises(_m_forwarg.UnknownArgumentError):
        parser_dash.parse_args(shlex.split('-f ---- --foo'))


# TODO: Compare all the results with argparse (they must behave the same)
#@pytest.fixture(params = [_m_argparse, _m_forwarg])
@pytest.fixture(params=[_m_forwarg])
def parser_plus(request):
    parser = request.param.ArgumentParser(prefix_chars='+')
    parser.add_argument('+O', action='store_false')
    parser.add_argument('+P', action='store_true')
    return parser


def test_plus_1(parser_plus):
    assert parser_plus.parse_args(shlex.split('+O +P')).namespace == \
                                        _m_argparse.Namespace(O=False, P=True)

# TODO: Add more tests...
#       Note that mixing different prefix characters is not fully supported
#       yet, in fact the options are stored in the parser object without the
#       prefix
