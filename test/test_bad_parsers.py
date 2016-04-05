import pytest
import shlex

from . import forwarg as _m_forwarg
import argparse as _m_argparse


def test1():
    parser = _m_forwarg.ArgumentParser()
    with pytest.raises(_m_forwarg.MultiplePositionalArgumentNamesError):
        parser.add_argument('pos', '-O')

# TODO: Add more tests...
