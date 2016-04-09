import pytest
import shlex

from . import forwarg as _m_forwarg
import argparse as _m_argparse


@pytest.fixture
def remainder_pos(parser):
    parser.add_argument('pos1')
    parser.add_argument('pos2')
    # TODO: This won't work when tests on argparse will be enabled
    parser.add_argument('posR', nargs=_m_forwarg.REMAINDER)
    parser.add_argument('-o', '--opt1')
    parser.add_argument('-p', '--opt2')
    return parser


@pytest.fixture
def remainder_opt(parser):
    parser.add_argument('pos1')
    parser.add_argument('pos2')
    parser.add_argument('-o', '--opt1')
    parser.add_argument('-p', '--opt2')
    # TODO: This won't work when tests on argparse will be enabled
    parser.add_argument('-R', '--optR', nargs=_m_forwarg.REMAINDER)
    return parser


@pytest.fixture
def remainder_both(parser):
    parser.add_argument('pos1')
    parser.add_argument('pos2')
    # TODO: This won't work when tests on argparse will be enabled
    parser.add_argument('posR', nargs=_m_forwarg.REMAINDER)
    parser.add_argument('-o', '--opt1')
    parser.add_argument('-p', '--opt2')
    # TODO: This won't work when tests on argparse will be enabled
    parser.add_argument('-R', '--optR', nargs=_m_forwarg.REMAINDER)
    return parser


def test_remainder_pos_1(remainder_pos):
    ns = remainder_pos.parse_args(shlex.split('xyz --opt1 foo bar abc --opt1 '
                                              '-pbar')).namespace
    assert ns == _m_argparse.Namespace(opt1='foo', opt2=None, pos1='xyz',
                                       pos2='bar', posR=['abc', '--opt1',
                                                         '-pbar'])


def test_remainder_opt_1(remainder_opt):
    ns = remainder_opt.parse_args(shlex.split('--opt2 foo bar xyz --optR abc '
                                              '--bar')).namespace
    assert ns == _m_argparse.Namespace(opt1=None, opt2='foo',
                                       optR=['abc', '--bar'],
                                       pos1='bar', pos2='xyz')


def test_remainder_opt_2(remainder_opt):
    ns = remainder_opt.parse_args(shlex.split('--opt2 foo bar xyz --optR=abc '
                                              '-Rbar')).namespace
    assert ns == _m_argparse.Namespace(opt1=None, opt2='foo',
                                       optR=['abc', '-Rbar'],
                                       pos1='bar', pos2='xyz')


def test_remainder_opt_3(remainder_opt):
    ns = remainder_opt.parse_args(shlex.split(
                                '--opt2 foo bar xyz -Rabc -R bar')).namespace
    assert ns == _m_argparse.Namespace(opt1=None, opt2='foo',
                                       optR=['abc', '-R', 'bar'],
                                       pos1='bar', pos2='xyz')


def test_remainder_opt_4(remainder_opt):
    ns = remainder_opt.parse_args(shlex.split(
                                '--opt2 foo bar xyz -Rabc -R=bar')).namespace
    assert ns == _m_argparse.Namespace(opt1=None, opt2='foo',
                                       optR=['abc', '-R=bar'],
                                       pos1='bar', pos2='xyz')


def test_remainder_opt_5(remainder_opt):
    ns = remainder_opt.parse_args(shlex.split(
                                '--opt2 foo bar xyz -Rabc -Rbar')).namespace
    assert ns == _m_argparse.Namespace(opt1=None, opt2='foo',
                                       optR=['abc', '-Rbar'],
                                       pos1='bar', pos2='xyz')


def test_remainder_opt_6(remainder_opt):
    ns = remainder_opt.parse_args(shlex.split('--opt2 foo bar xyz --optR abc '
                                              '--optR=bar')).namespace
    assert ns == _m_argparse.Namespace(opt1=None, opt2='foo',
                                       optR=['abc', '--optR=bar'],
                                       pos1='bar', pos2='xyz')


def test_remainder_opt_7(remainder_opt):
    ns = remainder_opt.parse_args(shlex.split('--opt2 foo bar xyz --optR abc '
                                              '-Rbar')).namespace
    assert ns == _m_argparse.Namespace(opt1=None, opt2='foo',
                                       optR=['abc', '-Rbar'],
                                       pos1='bar', pos2='xyz')


def test_remainder_both_1(remainder_both):
    ns = remainder_both.parse_args(shlex.split(
                    '--opt1 foo bar xyz abc --optR -p def --pbar')).namespace
    assert ns == _m_argparse.Namespace(opt1='foo', opt2=None, optR=None,
                                       pos1='bar', pos2='xyz',
                                       posR=['abc', '--optR', '-p', 'def',
                                             '--pbar'])
