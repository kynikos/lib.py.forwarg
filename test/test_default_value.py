import pytest
import shlex

from . import forwarg as _m_forwarg
import argparse as _m_argparse


@pytest.fixture
def opt1(parser):
    parser.add_argument('-O', default=10)
    return parser


def test1(opt1):
    assert opt1.parse_args(shlex.split('')).namespace == _m_argparse.Namespace(
                                                                        O=10)

# TODO: Add more tests...
