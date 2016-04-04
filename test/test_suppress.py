import pytest
import shlex

from . import forwarg as _m_forwarg
import argparse as _m_argparse


@pytest.fixture
def suppress(parser):
    group1 = parser.add_argument_group('group1', 'description1')
    group1.add_argument('pos1')
    # TODO: This won't work when tests on argparse will be enabled
    group1.add_argument('posS', default=_m_forwarg.SUPPRESS)
    group1.add_argument('pos2')
    group1.add_argument('-o', '--opt1')
    # TODO: This won't work when tests on argparse will be enabled
    group1.add_argument('-S', '--optS', default=_m_forwarg.SUPPRESS)
    group1.add_argument('-p', '--opt2')
    return parser


def test_suppress_1(suppress):
    ns = suppress.parse_args(shlex.split('--opt1 foo bar --optS xyz abc '
                                         '-p def ghi'))
    assert ns == _m_argparse.Namespace(opt1='foo', opt2='def', pos1='bar',
                                       pos2='ghi')
