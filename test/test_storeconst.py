import pytest
import shlex

from . import forwarg as _m_forwarg
import argparse as _m_argparse


@pytest.fixture
def const(parser):
    parser.add_argument('-O', action='store_const', const=10)
    return parser


def test1(const):
    assert const.parse_args(shlex.split('-O')).namespace == \
        _m_argparse.Namespace(O=10)

# TODO: Add more tests...
