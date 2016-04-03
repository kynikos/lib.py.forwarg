import pytest
import shlex

from . import forwarg as _m_forwarg
import argparse as _m_argparse


def test_check_duplicated_flags(_2_optional_arguments):
    for parser in _2_optional_arguments:
        with pytest.raises(_m_forwarg.InsufficientArgumentsError):
            parser.parse_args(shlex.split('--opt1 --opt2 foo --opt1 bar'))
