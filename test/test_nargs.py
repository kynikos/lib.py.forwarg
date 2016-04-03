import pytest
import shlex

from . import forwarg as _m_forwarg
import argparse as _m_argparse


@pytest.fixture
def posNone(parsers):
    for parser in parsers:
        group1 = parser.add_argument_group('group1', 'description1')
        group1.add_argument('posNone')

    return parsers


def test_posNone_1(posNone):
    for parser in posNone:
        with pytest.raises(_m_forwarg.InsufficientArgumentsError):
            parser.parse_args(shlex.split(''))


def test_posNone_2(posNone):
    for parser in posNone:
        assert parser.parse_args(shlex.split('foo')) == \
                                        _m_argparse.Namespace(posNone='foo')


def test_posNone_3(posNone):
    for parser in posNone:
        with pytest.raises(_m_forwarg.UnknownArgumentError):
            parser.parse_args(shlex.split('foo bar'))


@pytest.fixture
def posQues(parsers):
    for parser in parsers:
        group1 = parser.add_argument_group('group1', 'description1')
        group1.add_argument('posQues', nargs='?')

    return parsers


def test_posQues_1(posQues):
    for parser in posQues:
        assert parser.parse_args(shlex.split('')) == \
                                        _m_argparse.Namespace(posQues=None)


def test_posQues_2(posQues):
    for parser in posQues:
        assert parser.parse_args(shlex.split('foo')) == \
                                        _m_argparse.Namespace(posQues='foo')


def test_posQues_3(posQues):
    for parser in posQues:
        with pytest.raises(_m_forwarg.UnknownArgumentError):
            parser.parse_args(shlex.split('foo bar'))


@pytest.fixture
def posQuesC(parsers):
    for parser in parsers:
        group1 = parser.add_argument_group('group1', 'description1')
        group1.add_argument('posQuesC', nargs='?', const='CONST')

    return parsers


def test_posQuesC_1(posQuesC):
    for parser in posQuesC:
        assert parser.parse_args(shlex.split('')) == \
                                        _m_argparse.Namespace(posQuesC='CONST')


def test_posQuesC_2(posQuesC):
    for parser in posQuesC:
        assert parser.parse_args(shlex.split('foo')) == \
                                        _m_argparse.Namespace(posQuesC='foo')


def test_posQuesC_3(posQuesC):
    for parser in posQuesC:
        with pytest.raises(_m_forwarg.UnknownArgumentError):
            parser.parse_args(shlex.split('foo bar'))


@pytest.fixture
def posStar(parsers):
    for parser in parsers:
        group1 = parser.add_argument_group('group1', 'description1')
        group1.add_argument('posStar', nargs='*')

    return parsers


def test_posStar_1(posStar):
    for parser in posStar:
        assert parser.parse_args(shlex.split('')) == \
                                        _m_argparse.Namespace(posStar=None)


def test_posStar_2(posStar):
    for parser in posStar:
        assert parser.parse_args(shlex.split('foo')) == \
                                        _m_argparse.Namespace(posStar=['foo'])


def test_posStar_3(posStar):
    for parser in posStar:
        assert parser.parse_args(shlex.split('foo barbar33')) == \
                            _m_argparse.Namespace(posStar=['foo', 'barbar33'])


def test_posStar_4(posStar):
    for parser in posStar:
        assert parser.parse_args(shlex.split('foo barabc xyz 1 *^%')) == \
                        _m_argparse.Namespace(posStar=['foo', 'barabc',
                                                       'xyz', '1', '*^%'])


@pytest.fixture
def posPlus(parsers):
    for parser in parsers:
        group1 = parser.add_argument_group('group1', 'description1')
        group1.add_argument('posPlus', nargs='+')

    return parsers


def test_posPlus_1(posPlus):
    for parser in posPlus:
        with pytest.raises(_m_forwarg.InsufficientArgumentsError):
            parser.parse_args(shlex.split(''))


def test_posPlus_2(posPlus):
    for parser in posPlus:
        assert parser.parse_args(shlex.split('foo')) == \
                                        _m_argparse.Namespace(posPlus=['foo'])


def test_posPlus_3(posPlus):
    for parser in posPlus:
        assert parser.parse_args(shlex.split('foo barbar33')) == \
                            _m_argparse.Namespace(posPlus=['foo', 'barbar33'])


def test_posPlus_4(posPlus):
    for parser in posPlus:
        assert parser.parse_args(shlex.split('foo barabc xyz 1 *^%')) == \
                        _m_argparse.Namespace(posPlus=['foo', 'barabc',
                                                       'xyz', '1', '*^%'])


@pytest.fixture
def posRema(parsers):
    for parser in parsers:
        group1 = parser.add_argument_group('group1', 'description1')
        group1.add_argument('posRema', nargs=_m_forwarg.REMAINDER)

    return parsers


def test_posRema_1(posRema):
    for parser in posRema:
        with pytest.raises(_m_forwarg.InsufficientArgumentsError):
            parser.parse_args(shlex.split(''))


def test_posRema_2(posRema):
    for parser in posRema:
        assert parser.parse_args(shlex.split('foo')) == \
                                        _m_argparse.Namespace(posRema=['foo'])


def test_posRema_3(posRema):
    for parser in posRema:
        assert parser.parse_args(shlex.split('foo barbar33')) == \
                            _m_argparse.Namespace(posRema=['foo', 'barbar33'])


def test_posRema_4(posRema):
    for parser in posRema:
        assert parser.parse_args(shlex.split('foo barabc xyz 1 *^%')) == \
                        _m_argparse.Namespace(posRema=['foo', 'barabc',
                                                       'xyz', '1', '*^%'])


@pytest.fixture
def pos0(parsers):
    for parser in parsers:
        group1 = parser.add_argument_group('group1', 'description1')
        group1.add_argument('pos0', nargs=0)

    return parsers


def test_pos0_1(pos0):
    for parser in pos0:
        assert parser.parse_args(shlex.split('')) == \
                                        _m_argparse.Namespace(pos0=None)


def test_pos0_2(pos0):
    for parser in pos0:
        with pytest.raises(_m_forwarg.UnknownArgumentError):
            parser.parse_args(shlex.split('foo'))


def test_pos0_3(pos0):
    for parser in pos0:
        with pytest.raises(_m_forwarg.UnknownArgumentError):
            parser.parse_args(shlex.split('foo bar'))


@pytest.fixture
def pos1(parsers):
    for parser in parsers:
        group1 = parser.add_argument_group('group1', 'description1')
        group1.add_argument('pos1', nargs=1)

    return parsers


def test_pos1_1(pos1):
    for parser in pos1:
        with pytest.raises(_m_forwarg.InsufficientArgumentsError):
            parser.parse_args(shlex.split(''))


def test_pos1_2(pos1):
    for parser in pos1:
        assert parser.parse_args(shlex.split('foo')) == \
                                        _m_argparse.Namespace(pos1=['foo'])


def test_pos1_3(pos1):
    for parser in pos1:
        with pytest.raises(_m_forwarg.UnknownArgumentError):
            parser.parse_args(shlex.split('foo bar'))


@pytest.fixture
def pos2(parsers):
    for parser in parsers:
        group1 = parser.add_argument_group('group1', 'description1')
        group1.add_argument('pos2', nargs=2)

    return parsers


def test_pos2_1(pos2):
    for parser in pos2:
        with pytest.raises(_m_forwarg.InsufficientArgumentsError):
            parser.parse_args(shlex.split(''))


def test_pos2_2(pos2):
    for parser in pos2:
        with pytest.raises(_m_forwarg.InsufficientArgumentsError):
            parser.parse_args(shlex.split('foo'))


def test_pos2_3(pos2):
    for parser in pos2:
        assert parser.parse_args(shlex.split('foo bar')) == \
                                    _m_argparse.Namespace(pos2=['foo', 'bar'])


def test_pos2_4(pos2):
    for parser in pos2:
        with pytest.raises(_m_forwarg.UnknownArgumentError):
            parser.parse_args(shlex.split('foo bar xyz'))


@pytest.fixture
def pos5(parsers):
    for parser in parsers:
        group1 = parser.add_argument_group('group1', 'description1')
        group1.add_argument('pos5', nargs=5)

    return parsers


def test_pos5_1(pos5):
    for parser in pos5:
        with pytest.raises(_m_forwarg.InsufficientArgumentsError):
            parser.parse_args(shlex.split(''))


def test_pos5_2(pos5):
    for parser in pos5:
        with pytest.raises(_m_forwarg.InsufficientArgumentsError):
            parser.parse_args(shlex.split('foo bar abc def'))


def test_pos5_3(pos5):
    for parser in pos5:
        assert parser.parse_args(shlex.split('foo bar abc def xyz')) == \
                _m_argparse.Namespace(pos5=['foo', 'bar', 'abc', 'def', 'xyz'])


def test_pos5_4(pos5):
    for parser in pos5:
        with pytest.raises(_m_forwarg.UnknownArgumentError):
            parser.parse_args(shlex.split('foo bar abc def xyz qrs'))


@pytest.fixture
def optNone(parsers):
    for parser in parsers:
        group1 = parser.add_argument_group('group1', 'description1')
        group1.add_argument('-N', '--optNone')

    return parsers


def test_optNone_1(optNone):
    for parser in optNone:
        assert parser.parse_args(shlex.split('')) == \
                                        _m_argparse.Namespace(optNone=None)


def test_optNone_2(optNone):
    for parser in optNone:
        with pytest.raises(_m_forwarg.InsufficientArgumentsError):
            parser.parse_args(shlex.split('-N'))


def test_optNone_3(optNone):
    for parser in optNone:
        assert parser.parse_args(shlex.split('-N foo')) == \
                                        _m_argparse.Namespace(optNone='foo')


def test_optNone_4(optNone):
    for parser in optNone:
        with pytest.raises(_m_forwarg.UnknownArgumentError):
            parser.parse_args(shlex.split('-N foo bar'))


@pytest.fixture
def optQues(parsers):
    for parser in parsers:
        group1 = parser.add_argument_group('group1', 'description1')
        group1.add_argument('-Q', '--optQues', nargs='?')

    return parsers


def test_optQues_1(optQues):
    for parser in optQues:
        assert parser.parse_args(shlex.split('')) == \
                                        _m_argparse.Namespace(optQues=None)


def test_optQues_2(optQues):
    for parser in optQues:
        assert parser.parse_args(shlex.split('-Q')) == \
                                        _m_argparse.Namespace(optQues=None)


def test_optQues_3(optQues):
    for parser in optQues:
        assert parser.parse_args(shlex.split('-Q foo')) == \
                                        _m_argparse.Namespace(optQues='foo')


def test_optQues_4(optQues):
    for parser in optQues:
        with pytest.raises(_m_forwarg.UnknownArgumentError):
            parser.parse_args(shlex.split('-Q foo bar'))


@pytest.fixture
def optQuesC(parsers):
    for parser in parsers:
        group1 = parser.add_argument_group('group1', 'description1')
        group1.add_argument('-C', '--optQuesC', nargs='?', const='CONST')

    return parsers


def test_optQuesC_1(optQuesC):
    for parser in optQuesC:
        assert parser.parse_args(shlex.split('')) == \
                                        _m_argparse.Namespace(optQuesC=None)


def test_optQuesC_2(optQuesC):
    for parser in optQuesC:
        assert parser.parse_args(shlex.split('-C')) == \
                                        _m_argparse.Namespace(optQuesC='CONST')


def test_optQuesC_3(optQuesC):
    for parser in optQuesC:
        assert parser.parse_args(shlex.split('-C foo')) == \
                                        _m_argparse.Namespace(optQuesC='foo')


def test_optQuesC_4(optQuesC):
    for parser in optQuesC:
        with pytest.raises(_m_forwarg.UnknownArgumentError):
            parser.parse_args(shlex.split('-C foo bar'))


@pytest.fixture
def optStar(parsers):
    for parser in parsers:
        group1 = parser.add_argument_group('group1', 'description1')
        group1.add_argument('-S', '--optStar', nargs='*')

    return parsers


def test_optStar_1(optStar):
    for parser in optStar:
        assert parser.parse_args(shlex.split('')) == \
                                        _m_argparse.Namespace(optStar=None)


def test_optStar_2(optStar):
    for parser in optStar:
        assert parser.parse_args(shlex.split('-S')) == \
                                        _m_argparse.Namespace(optStar=[])


def test_optStar_3(optStar):
    for parser in optStar:
        assert parser.parse_args(shlex.split('-S foo')) == \
                                        _m_argparse.Namespace(optStar=['foo'])


def test_optStar_4(optStar):
    for parser in optStar:
        assert parser.parse_args(shlex.split('-S foo bar xyz abc')) == \
                    _m_argparse.Namespace(optStar=['foo', 'bar', 'xyz', 'abc'])


@pytest.fixture
def optPlus(parsers):
    for parser in parsers:
        group1 = parser.add_argument_group('group1', 'description1')
        group1.add_argument('-P', '--optPlus', nargs='+')

    return parsers


# TODO


@pytest.fixture
def optRema(parsers):
    for parser in parsers:
        group1 = parser.add_argument_group('group1', 'description1')
        group1.add_argument('-R', '--optRema', nargs=_m_forwarg.REMAINDER)

    return parsers


# TODO


@pytest.fixture
def opt0(parsers):
    for parser in parsers:
        group1 = parser.add_argument_group('group1', 'description1')
        group1.add_argument('-0', '--opt0', nargs=0)

    return parsers


# TODO


@pytest.fixture
def opt1(parsers):
    for parser in parsers:
        group1 = parser.add_argument_group('group1', 'description1')
        group1.add_argument('-1', '--opt1', nargs=1)

    return parsers


# TODO


@pytest.fixture
def opt2(parsers):
    for parser in parsers:
        group1 = parser.add_argument_group('group1', 'description1')
        group1.add_argument('-2', '--opt2', nargs=2)

    return parsers


# TODO


@pytest.fixture
def opt5(parsers):
    for parser in parsers:
        group1 = parser.add_argument_group('group1', 'description1')
        group1.add_argument('-5', '--opt5', nargs=5)

    return parsers


# TODO


@pytest.fixture
def complex(parsers):
    for parser in parsers:
        group1 = parser.add_argument_group('group1', 'description1')
        group1.add_argument('posNone')
        group1.add_argument('posQues', nargs='?')
        group1.add_argument('posQuesC', nargs='?', const='CONST')
        group1.add_argument('posStar', nargs='*')
        group1.add_argument('posPlus', nargs='+')
        group1.add_argument('posRema', nargs=_m_forwarg.REMAINDER)
        group1.add_argument('pos0', nargs=0)
        group1.add_argument('pos1', nargs=1)
        group1.add_argument('pos2', nargs=2)
        group1.add_argument('pos5', nargs=5)
        group1.add_argument('-N', '--optNone')
        group1.add_argument('-Q', '--optQues', nargs='?')
        group1.add_argument('-C', '--optQuesC', nargs='?', const='CONST')
        group1.add_argument('-S', '--optStar', nargs='*')
        group1.add_argument('-P', '--optPlus', nargs='+')
        group1.add_argument('-R', '--optRema', nargs=_m_forwarg.REMAINDER)
        group1.add_argument('-0', '--opt0', nargs=0)
        group1.add_argument('-1', '--opt1', nargs=1)
        group1.add_argument('-2', '--opt2', nargs=2)
        group1.add_argument('-5', '--opt5', nargs=5)

    return parsers


# TODO
