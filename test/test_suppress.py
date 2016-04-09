import pytest
import shlex

from . import forwarg as _m_forwarg
import argparse as _m_argparse


@pytest.fixture
def suppress(parser):
    parser.add_argument('pos1')
    # TODO: This won't work when tests on argparse will be enabled
    parser.add_argument('posS', default=_m_forwarg.SUPPRESS)
    parser.add_argument('pos2')
    parser.add_argument('-o', '--opt1')
    # TODO: This won't work when tests on argparse will be enabled
    parser.add_argument('-S', '--optS', default=_m_forwarg.SUPPRESS)
    parser.add_argument('-p', '--opt2')
    return parser


def test_suppress_1(suppress):
    ns = suppress.parse_args(shlex.split('--opt1 foo bar --optS xyz abc '
                                         '-p def ghi')).namespace
    assert ns == _m_argparse.Namespace(opt1='foo', opt2='def', pos1='bar',
                                       pos2='ghi')
