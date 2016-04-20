import pytest
import shlex

from . import forwarg as _m_forwarg
import argparse as _m_argparse


@pytest.fixture
def case_1(parser):
    parser.add_argument('-o', '--opt')
    return parser


def test_1(case_1):
    ns = case_1.parse_args(shlex.split('--opt "foo bar"')).namespace
    assert ns == _m_argparse.Namespace(opt='foo bar')


def test_2(case_1):
    ns = case_1.parse_args(shlex.split("--opt 'foo bar'")).namespace
    assert ns == _m_argparse.Namespace(opt='foo bar')


def test_3(case_1):
    ns = case_1.parse_args(shlex.split('--opt="foo bar"')).namespace
    assert ns == _m_argparse.Namespace(opt='foo bar')


def test_4(case_1):
    ns = case_1.parse_args(shlex.split("--opt='foo bar'")).namespace
    assert ns == _m_argparse.Namespace(opt='foo bar')


def test_5(case_1):
    ns = case_1.parse_args(shlex.split('-o "foo bar"')).namespace
    assert ns == _m_argparse.Namespace(opt='foo bar')


def test_6(case_1):
    ns = case_1.parse_args(shlex.split("-o 'foo bar'")).namespace
    assert ns == _m_argparse.Namespace(opt='foo bar')


def test_7(case_1):
    ns = case_1.parse_args(shlex.split('-o"foo bar"')).namespace
    assert ns == _m_argparse.Namespace(opt='foo bar')


def test_8(case_1):
    ns = case_1.parse_args(shlex.split("-o'foo bar'")).namespace
    assert ns == _m_argparse.Namespace(opt='foo bar')


@pytest.fixture
def case_2(parser):
    parser.add_argument('pos')
    return parser


def test_9(case_2):
    ns = case_2.parse_args(shlex.split('"foo bar"')).namespace
    assert ns == _m_argparse.Namespace(pos='foo bar')


def test_10(case_2):
    ns = case_2.parse_args(shlex.split("'foo bar'")).namespace
    assert ns == _m_argparse.Namespace(pos='foo bar')
