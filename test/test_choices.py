import pytest
import shlex

from . import forwarg as _m_forwarg
import argparse as _m_argparse


@pytest.fixture
def opt1(parser):
    parser.add_argument('-O', choices=('a', 'foo', '42'))
    return parser


def test_1(opt1):
    with pytest.raises(_m_forwarg.InvalidArgumentError):
        opt1.parse_args(shlex.split('-O bar'))

# TODO: Add more tests...
