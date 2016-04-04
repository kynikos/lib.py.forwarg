import pytest
import shlex

from . import forwarg as _m_forwarg
import argparse as _m_argparse


@pytest.fixture
def pos1(parser):
    parser.add_argument('arg', nargs='*')
    return parser


def test1(pos1):
    assert pos1.parse_args(shlex.split('foo -- --bar')) == \
                                    _m_argparse.Namespace(arg=['foo', '--bar'])

# TODO: Add more tests...
