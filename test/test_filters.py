import pytest
import shlex

from . import forwarg as _m_forwarg
import argparse as _m_argparse


@pytest.fixture
def parser_1(parser):
    group1 = parser.add_argument_group('one')
    group1.add_argument('pos1')
    group1.add_argument('-o', '--opt1')
    group2 = parser.add_argument_group('two')
    group2.add_argument('pos2', nargs='*')
    group2.add_argument('-p', '--opt2')
    return parser


@pytest.fixture
def command_1(parser_1):
    res = parser_1.parse_args(shlex.split('--opt1 foo bar abc -p def -- -ghi'))
    return res


def test_whitelist_1(command_1):
    assert ' '.join(command_1.filter_whitelist()) == ''


def test_whitelist_2(command_1):
    assert ' '.join(command_1.filter_whitelist(dests=('pos1', ))) == 'bar'


def test_whitelist_3(command_1):
    assert ' '.join(command_1.filter_whitelist(dests=('pos2', 'opt1'))) == \
        '--opt1 foo abc -- -ghi'


def test_whitelist_4(command_1):
    assert ' '.join(command_1.filter_whitelist(groups=('one', ))) == \
        '--opt1 foo bar'


def test_whitelist_5(command_1):
    assert ' '.join(command_1.filter_whitelist(groups=('two', 'one'))) == \
        '--opt1 foo bar abc -p def -- -ghi'


def test_whitelist_6(command_1):
    assert ' '.join(command_1.filter_whitelist(dests=('pos1'),
                                               groups=('two'))) == \
                                               'bar abc -p def -- -ghi'


def test_blacklist_1(command_1):
    assert ' '.join(command_1.filter_blacklist()) == \
        '--opt1 foo bar abc -p def -- -ghi'


def test_blacklist_2(command_1):
    assert ' '.join(command_1.filter_blacklist(dests=('pos1', ))) == \
        '--opt1 foo abc -p def -- -ghi'


def test_blacklist_3(command_1):
    assert ' '.join(command_1.filter_blacklist(dests=('pos2', 'opt1'))) == \
        'bar -p def'


def test_blacklist_4(command_1):
    assert ' '.join(command_1.filter_blacklist(groups=('one', ))) == \
        'abc -p def -- -ghi'


def test_blacklist_5(command_1):
    assert ' '.join(command_1.filter_blacklist(groups=('two', 'one'))) == ''


def test_blacklist_6(command_1):
    assert ' '.join(command_1.filter_blacklist(dests=('pos1'),
                                               groups=('two'))) == \
                                               '--opt1 foo'


@pytest.fixture
def command_2(parser_1):
    res = parser_1.parse_args(shlex.split('--opt1 foo bar abc -p def'))
    return res


def test_whitelist_7(command_2):
    assert ' '.join(command_2.filter_whitelist(dests=('pos2'))) == 'abc'


def test_blacklist_8(command_2):
    assert ' '.join(command_2.filter_blacklist(dests=('pos2'))) == \
        '--opt1 foo bar -p def'


@pytest.fixture
def parser_2(parser):
    parser.add_argument('pos1')
    parser.add_argument('pos2', nargs='*')
    parser.add_argument('-o', '--opt1')
    parser.add_argument('-p', '--opt2', action='store_true')
    parser.add_argument('-q', '--opt3', action='store_true')
    parser.add_argument('-r', '--opt4')
    return parser


@pytest.fixture
def command_2_1(parser_2):
    res = parser_2.parse_args(shlex.split('foo -qpo=bar abc -r def'))
    return res


def test_whitelist_2_1_1(command_2_1):
    assert ' '.join(command_2_1.filter_whitelist(dests=('opt1'))) == '-o=bar'


def test_whitelist_2_1_2(command_2_1):
    assert ' '.join(command_2_1.filter_whitelist(dests=('opt2'))) == '-p'


def test_whitelist_2_1_3(command_2_1):
    assert ' '.join(command_2_1.filter_whitelist(dests=('opt3'))) == '-q'


def test_blacklist_2_1_1(command_2_1):
    assert ' '.join(command_2_1.filter_blacklist(dests=('opt1'))) == \
        'foo -qp abc -r def'


def test_blacklist_2_1_2(command_2_1):
    assert ' '.join(command_2_1.filter_blacklist(dests=('opt2'))) == \
        'foo -qo=bar abc -r def'


def test_blacklist_2_1_3(command_2_1):
    assert ' '.join(command_2_1.filter_blacklist(dests=('opt3'))) == \
        'foo -po=bar abc -r def'
