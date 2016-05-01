import pytest
import shlex

from . import forwarg as _m_forwarg
import argparse as _m_argparse


@pytest.fixture
def pos1(parser):
    parser.add_argument('arg', nargs='*')
    return parser


def test_pos1_1(pos1):
    assert pos1.parse_args(shlex.split('--')).namespace == \
                                                _m_argparse.Namespace(arg=None)


def test_pos1_2(pos1):
    assert pos1.parse_args(shlex.split('-- --bar')).namespace == \
                                        _m_argparse.Namespace(arg=['--bar'])


def test_pos1_3(pos1):
    assert pos1.parse_args(shlex.split('foo --')).namespace == \
                                            _m_argparse.Namespace(arg=['foo'])


def test_pos1_4(pos1):
    assert pos1.parse_args(shlex.split('foo -- --bar')).namespace == \
                                    _m_argparse.Namespace(arg=['foo', '--bar'])


@pytest.fixture
def opt1(parser):
    parser.add_argument('arg', nargs='*')
    parser.add_argument('-f', '--foo', action='store_true')
    return parser


def test_opt1_1(opt1):
    assert opt1.parse_args(shlex.split('--')).namespace == \
                                    _m_argparse.Namespace(arg=None, foo=None)


def test_opt1_2(opt1):
    assert opt1.parse_args(shlex.split('-- --foo')).namespace == \
                                _m_argparse.Namespace(arg=['--foo'], foo=None)


def test_opt1_3(opt1):
    assert opt1.parse_args(shlex.split('--foo --')).namespace == \
                                    _m_argparse.Namespace(arg=None, foo=True)


def test_opt1_4(opt1):
    assert opt1.parse_args(shlex.split('-f -- --foo')).namespace == \
                                _m_argparse.Namespace(arg=['--foo'], foo=True)
