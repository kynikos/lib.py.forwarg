import pytest
import shlex

from . import forwarg as _m_forwarg
import argparse as _m_argparse


@pytest.fixture
def parser():
    # TODO: Compare with argparse
    parser = _m_forwarg.ArgumentParser(prefix_chars='-+')
    parser.add_argument('-O', action='store_false')
    parser.add_argument('+O', action='store_true', dest='OO')
    return parser


def test1(parser):
    assert parser.parse_args(shlex.split('-O +O')) == _m_argparse.Namespace(
                                                            O=False, OO=True)

# TODO: Add more tests...
