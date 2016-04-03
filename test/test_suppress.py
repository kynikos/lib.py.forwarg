import pytest
import shlex

from . import forwarg as _m_forwarg
import argparse as _m_argparse


def test_suppress_1(suppress):
    for parser in suppress:
        ns = parser.parse_args(shlex.split('--opt1 foo bar --optS xyz abc '
                                           '-p def ghi'))
        assert ns == _m_argparse.Namespace(opt1='foo', opt2='def', pos1='bar',
                                           pos2='ghi')
