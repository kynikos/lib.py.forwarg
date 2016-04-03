import pytest
import shlex

from . import forwarg as _m_forwarg
import argparse as _m_argparse


def test_remainder_pos_1(remainder_pos):
    for parser in remainder_pos:
        ns = parser.parse_args(shlex.split('xyz --opt1 foo bar abc --opt1 '
                                           '-pbar'))
        assert ns == _m_argparse.Namespace(opt1='foo', opt2=None, pos1='xyz',
                                           pos2='bar', posR=['abc', '--opt1',
                                                             '-pbar'])


def test_remainder_opt_1(remainder_opt):
    for parser in remainder_opt:
        ns = parser.parse_args(shlex.split('--opt2 foo bar xyz --optR abc '
                                           '--bar'))
        assert ns == _m_argparse.Namespace(opt1=None, opt2='foo',
                                           optR=['abc', '--bar'],
                                           pos1='bar', pos2='xyz')


def test_remainder_opt_2(remainder_opt):
    for parser in remainder_opt:
        ns = parser.parse_args(shlex.split('--opt2 foo bar xyz --optR=abc '
                                           '-Rbar'))
        assert ns == _m_argparse.Namespace(opt1=None, opt2='foo',
                                           optR=['abc', '-Rbar'],
                                           pos1='bar', pos2='xyz')


def test_remainder_opt_3(remainder_opt):
    for parser in remainder_opt:
        ns = parser.parse_args(shlex.split('--opt2 foo bar xyz -Rabc -R bar'))
        assert ns == _m_argparse.Namespace(opt1=None, opt2='foo',
                                           optR=['abc', '-R', 'bar'],
                                           pos1='bar', pos2='xyz')


def test_remainder_opt_4(remainder_opt):
    for parser in remainder_opt:
        ns = parser.parse_args(shlex.split('--opt2 foo bar xyz -Rabc -R=bar'))
        assert ns == _m_argparse.Namespace(opt1=None, opt2='foo',
                                           optR=['abc', '-R=bar'],
                                           pos1='bar', pos2='xyz')


def test_remainder_opt_5(remainder_opt):
    for parser in remainder_opt:
        ns = parser.parse_args(shlex.split('--opt2 foo bar xyz -Rabc -Rbar'))
        assert ns == _m_argparse.Namespace(opt1=None, opt2='foo',
                                           optR=['abc', '-Rbar'],
                                           pos1='bar', pos2='xyz')


def test_remainder_opt_6(remainder_opt):
    for parser in remainder_opt:
        ns = parser.parse_args(shlex.split('--opt2 foo bar xyz --optR abc '
                                           '--optR=bar'))
        assert ns == _m_argparse.Namespace(opt1=None, opt2='foo',
                                           optR=['abc', '--optR=bar'],
                                           pos1='bar', pos2='xyz')


def test_remainder_opt_7(remainder_opt):
    for parser in remainder_opt:
        ns = parser.parse_args(shlex.split('--opt2 foo bar xyz --optR abc '
                                           '-Rbar'))
        assert ns == _m_argparse.Namespace(opt1=None, opt2='foo',
                                           optR=['abc', '-Rbar'],
                                           pos1='bar', pos2='xyz')


def test_remainder_both_1(remainder_both):
    for parser in remainder_both:
        ns = parser.parse_args(shlex.split('--opt1 foo bar xyz abc --optR -p '
                                           'def --pbar'))
        assert ns == _m_argparse.Namespace(opt1='foo', opt2=None, optR=None,
                                           pos1='bar', pos2='xyz',
                                           posR=['abc', '--optR', '-p', 'def',
                                                 '--pbar'])
