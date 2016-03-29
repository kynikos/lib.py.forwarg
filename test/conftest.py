import pytest

from . import forwarg as _m_forwarg
import argparse as _m_argparse


@pytest.fixture
def parsers():
    FWparser = _m_forwarg.ArgumentParser()
    APparser = _m_argparse.ArgumentParser()

    return (FWparser, APparser)


@pytest.fixture
def _1_positional_argument(parsers):
    for parser in parsers:
        group1 = parser.add_argument_group('group1', 'description1')
        group1.add_argument('pos1')

    return parsers


@pytest.fixture
def _2_positional_arguments(parsers):
    for parser in parsers:
        group1 = parser.add_argument_group('group1', 'description1')
        group1.add_argument('pos1')
        group1.add_argument('pos2')

    return parsers