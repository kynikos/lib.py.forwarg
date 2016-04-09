import pytest
import shlex

from . import forwarg as _m_forwarg
import argparse as _m_argparse


def test1(parser):
    group1 = parser.add_argument_group('group1')
    group1.add_argument('arg')
    assert 'group1' in parser.title_to_group
    assert parser.dest_to_argdef['arg'].group is group1

# TODO: Add more tests...
