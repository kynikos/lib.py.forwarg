import pytest
import shlex

from . import forwarg as _m_forwarg
import argparse as _m_argparse


@pytest.fixture
def _1_optional_argument(parser):
    parser.add_argument('-o', '--opt1')
    return parser


def test_1(_1_optional_argument):
    ns = _1_optional_argument.parse_args(shlex.split('--opt1 foo')).namespace
    assert ns == _m_argparse.Namespace(opt1='foo')


def test_2(_1_optional_argument):
    ns = _1_optional_argument.parse_args(shlex.split('--opt1=foo')).namespace
    assert ns == _m_argparse.Namespace(opt1='foo')


def test_3(_1_optional_argument):
    ns = _1_optional_argument.parse_args(shlex.split('-o foo')).namespace
    assert ns == _m_argparse.Namespace(opt1='foo')


def test_4(_1_optional_argument):
    ns = _1_optional_argument.parse_args(shlex.split('-o=foo')).namespace
    assert ns == _m_argparse.Namespace(opt1='foo')


def test_5(_1_optional_argument):
    ns = _1_optional_argument.parse_args(shlex.split('-ofoo')).namespace
    assert ns == _m_argparse.Namespace(opt1='foo')
