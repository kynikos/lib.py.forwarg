import pytest
import shlex

from . import forwarg as _m_forwarg
import argparse as _m_argparse


def test_1(_1_optional_argument):
    for parser in _1_optional_argument:
        ns = parser.parse_args(shlex.split('--opt1 foo'))
        assert ns == _m_argparse.Namespace(opt1='foo')

        ns = parser.parse_args(shlex.split('--opt1=foo'))
        assert ns == _m_argparse.Namespace(opt1='foo')

        ns = parser.parse_args(shlex.split('-o foo'))
        assert ns == _m_argparse.Namespace(opt1='foo')

        ns = parser.parse_args(shlex.split('-o=foo'))
        assert ns == _m_argparse.Namespace(opt1='foo')

        ns = parser.parse_args(shlex.split('-ofoo'))
        assert ns == _m_argparse.Namespace(opt1='foo')
