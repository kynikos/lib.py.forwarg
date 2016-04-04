import pytest
import shlex

from . import forwarg as _m_forwarg
import argparse as _m_argparse


@pytest.fixture
def _2_optional_arguments(parser):
    group1 = parser.add_argument_group('group1', 'description1')
    group1.add_argument('-o', '--opt1')
    group1.add_argument('-p', '--opt2')
    return parser


def test_check_duplicated_flags(_2_optional_arguments):
    with pytest.raises(_m_forwarg.InsufficientArgumentsError):
        _2_optional_arguments.parse_args(shlex.split(
                                            '--opt1 --opt2 foo --opt1 bar'))
