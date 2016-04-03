import pytest

from . import forwarg as _m_forwarg
import argparse as _m_argparse


@pytest.fixture
def parsers():
    # TODO: Compare all the results with argparse (they must behave
    #       the same); in particular, reproduce all the examples in argparse's
    #       doc page

    # APparser = _m_argparse.ArgumentParser()
    FWparser = _m_forwarg.ArgumentParser()

    # return (APparser, FWparser)
    return (FWparser, )


@pytest.fixture
def no_arguments(parsers):
    for parser in parsers:
        parser.add_argument_group('group1', 'description1')

    return parsers


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


@pytest.fixture
def _1_optional_argument_long(parsers):
    for parser in parsers:
        group1 = parser.add_argument_group('group1', 'description1')
        group1.add_argument('--opt1')

    return parsers


@pytest.fixture
def _1_optional_argument_short(parsers):
    for parser in parsers:
        group1 = parser.add_argument_group('group1', 'description1')
        group1.add_argument('-o')

    return parsers


@pytest.fixture
def _1_optional_argument(parsers):
    for parser in parsers:
        group1 = parser.add_argument_group('group1', 'description1')
        group1.add_argument('-o', '--opt1')

    return parsers


@pytest.fixture
def _2_optional_arguments(parsers):
    for parser in parsers:
        group1 = parser.add_argument_group('group1', 'description1')
        group1.add_argument('-o', '--opt1')
        group1.add_argument('-p', '--opt2')

    return parsers


@pytest.fixture
def _2_mixed_arguments(parsers):
    for parser in parsers:
        group1 = parser.add_argument_group('group1', 'description1')
        group1.add_argument('pos1')
        group1.add_argument('-o', '--opt1')

    return parsers


@pytest.fixture
def remainder_pos(parsers):
    for parser in parsers:
        group1 = parser.add_argument_group('group1', 'description1')
        group1.add_argument('pos1')
        group1.add_argument('pos2')
        # TODO: This won't work when tests on argparse will be enabled
        group1.add_argument('posR', nargs=_m_forwarg.REMAINDER)
        group1.add_argument('-o', '--opt1')
        group1.add_argument('-p', '--opt2')

    return parsers


@pytest.fixture
def remainder_opt(parsers):
    for parser in parsers:
        group1 = parser.add_argument_group('group1', 'description1')
        group1.add_argument('pos1')
        group1.add_argument('pos2')
        group1.add_argument('-o', '--opt1')
        group1.add_argument('-p', '--opt2')
        # TODO: This won't work when tests on argparse will be enabled
        group1.add_argument('-R', '--optR', nargs=_m_forwarg.REMAINDER)

    return parsers


@pytest.fixture
def remainder_both(parsers):
    for parser in parsers:
        group1 = parser.add_argument_group('group1', 'description1')
        group1.add_argument('pos1')
        group1.add_argument('pos2')
        # TODO: This won't work when tests on argparse will be enabled
        group1.add_argument('posR', nargs=_m_forwarg.REMAINDER)
        group1.add_argument('-o', '--opt1')
        group1.add_argument('-p', '--opt2')
        # TODO: This won't work when tests on argparse will be enabled
        group1.add_argument('-R', '--optR', nargs=_m_forwarg.REMAINDER)

    return parsers


@pytest.fixture
def suppress(parsers):
    for parser in parsers:
        group1 = parser.add_argument_group('group1', 'description1')
        group1.add_argument('pos1')
        # TODO: This won't work when tests on argparse will be enabled
        group1.add_argument('posS', default=_m_forwarg.SUPPRESS)
        group1.add_argument('pos2')
        group1.add_argument('-o', '--opt1')
        # TODO: This won't work when tests on argparse will be enabled
        group1.add_argument('-S', '--optS', default=_m_forwarg.SUPPRESS)
        group1.add_argument('-p', '--opt2')

    return parsers
