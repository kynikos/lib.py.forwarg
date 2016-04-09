import pytest
import shlex

from . import forwarg as _m_forwarg
import argparse as _m_argparse


@pytest.fixture
def none(parser):
    parser.add_argument('-O', action='append')
    return parser


def test1(none):
    assert none.parse_args(shlex.split('-O foo -O bar')).namespace == \
                                        _m_argparse.Namespace(O=['foo', 'bar'])

# TODO: Add more tests...
