import pytest
import shlex

from . import forwarg as _m_forwarg
import argparse as _m_argparse


@pytest.fixture
def posNone(parser):
    parser.add_argument('posNone')
    return parser


def test_posNone_1(posNone):
    with pytest.raises(_m_forwarg.InsufficientArgumentsError):
        posNone.parse_args(shlex.split(''))


def test_posNone_2(posNone):
    assert posNone.parse_args(shlex.split('foo')) == _m_argparse.Namespace(
                                                                posNone='foo')


def test_posNone_3(posNone):
    with pytest.raises(_m_forwarg.UnknownArgumentError):
        posNone.parse_args(shlex.split('foo bar'))


@pytest.fixture
def posQues(parser):
    parser.add_argument('posQues', nargs='?')
    return parser


def test_posQues_1(posQues):
    assert posQues.parse_args(shlex.split('')) == _m_argparse.Namespace(
                                                                posQues=None)


def test_posQues_2(posQues):
    assert posQues.parse_args(shlex.split('foo')) == _m_argparse.Namespace(
                                                                posQues='foo')


def test_posQues_3(posQues):
    with pytest.raises(_m_forwarg.UnknownArgumentError):
        posQues.parse_args(shlex.split('foo bar'))


@pytest.fixture
def posQuesC(parser):
    parser.add_argument('posQuesC', nargs='?', const='CONST')
    return parser


def test_posQuesC_1(posQuesC):
    assert posQuesC.parse_args(shlex.split('')) == _m_argparse.Namespace(
                                                            posQuesC='CONST')


def test_posQuesC_2(posQuesC):
    assert posQuesC.parse_args(shlex.split('foo')) == _m_argparse.Namespace(
                                                                posQuesC='foo')


def test_posQuesC_3(posQuesC):
    with pytest.raises(_m_forwarg.UnknownArgumentError):
        posQuesC.parse_args(shlex.split('foo bar'))


@pytest.fixture
def posStar(parser):
    parser.add_argument('posStar', nargs='*')
    return parser


def test_posStar_1(posStar):
    assert posStar.parse_args(shlex.split('')) == _m_argparse.Namespace(
                                                                posStar=None)


def test_posStar_2(posStar):
    assert posStar.parse_args(shlex.split('foo')) == _m_argparse.Namespace(
                                                            posStar=['foo'])


def test_posStar_3(posStar):
    assert posStar.parse_args(shlex.split('foo barbar33')) == \
                            _m_argparse.Namespace(posStar=['foo', 'barbar33'])


def test_posStar_4(posStar):
    assert posStar.parse_args(shlex.split('foo barabc xyz 1 *^%')) == \
                            _m_argparse.Namespace(posStar=['foo', 'barabc',
                                                           'xyz', '1', '*^%'])


@pytest.fixture
def posPlus(parser):
    parser.add_argument('posPlus', nargs='+')
    return parser


def test_posPlus_1(posPlus):
    with pytest.raises(_m_forwarg.InsufficientArgumentsError):
        posPlus.parse_args(shlex.split(''))


def test_posPlus_2(posPlus):
    assert posPlus.parse_args(shlex.split('foo')) == _m_argparse.Namespace(
                                                            posPlus=['foo'])


def test_posPlus_3(posPlus):
    assert posPlus.parse_args(shlex.split('foo barbar33')) == \
                            _m_argparse.Namespace(posPlus=['foo', 'barbar33'])


def test_posPlus_4(posPlus):
    assert posPlus.parse_args(shlex.split('foo barabc xyz 1 *^%')) == \
                            _m_argparse.Namespace(posPlus=['foo', 'barabc',
                                                           'xyz', '1', '*^%'])


@pytest.fixture
def posRema(parser):
    parser.add_argument('posRema', nargs=_m_forwarg.REMAINDER)
    return parser


def test_posRema_1(posRema):
    with pytest.raises(_m_forwarg.InsufficientArgumentsError):
        posRema.parse_args(shlex.split(''))


def test_posRema_2(posRema):
    assert posRema.parse_args(shlex.split('foo')) == _m_argparse.Namespace(
                                                            posRema=['foo'])


def test_posRema_3(posRema):
    assert posRema.parse_args(shlex.split('foo barbar33')) == \
                            _m_argparse.Namespace(posRema=['foo', 'barbar33'])


def test_posRema_4(posRema):
    assert posRema.parse_args(shlex.split('foo barabc xyz 1 *^%')) == \
                            _m_argparse.Namespace(posRema=['foo', 'barabc',
                                                           'xyz', '1', '*^%'])


@pytest.fixture
def pos0(parser):
    parser.add_argument('pos0', nargs=0)
    return parser


def test_pos0_1(pos0):
    assert pos0.parse_args(shlex.split('')) == _m_argparse.Namespace(pos0=None)


def test_pos0_2(pos0):
    with pytest.raises(_m_forwarg.UnknownArgumentError):
        pos0.parse_args(shlex.split('foo'))


def test_pos0_3(pos0):
    with pytest.raises(_m_forwarg.UnknownArgumentError):
        pos0.parse_args(shlex.split('foo bar'))


@pytest.fixture
def pos1(parser):
    parser.add_argument('pos1', nargs=1)
    return parser


def test_pos1_1(pos1):
    with pytest.raises(_m_forwarg.InsufficientArgumentsError):
        pos1.parse_args(shlex.split(''))


def test_pos1_2(pos1):
    assert pos1.parse_args(shlex.split('foo')) == _m_argparse.Namespace(
                                                                pos1=['foo'])


def test_pos1_3(pos1):
    with pytest.raises(_m_forwarg.UnknownArgumentError):
        pos1.parse_args(shlex.split('foo bar'))


@pytest.fixture
def pos2(parser):
    parser.add_argument('pos2', nargs=2)
    return parser


def test_pos2_1(pos2):
    with pytest.raises(_m_forwarg.InsufficientArgumentsError):
        pos2.parse_args(shlex.split(''))


def test_pos2_2(pos2):
    with pytest.raises(_m_forwarg.InsufficientArgumentsError):
        pos2.parse_args(shlex.split('foo'))


def test_pos2_3(pos2):
    assert pos2.parse_args(shlex.split('foo bar')) == _m_argparse.Namespace(
                                                        pos2=['foo', 'bar'])


def test_pos2_4(pos2):
    with pytest.raises(_m_forwarg.UnknownArgumentError):
        pos2.parse_args(shlex.split('foo bar xyz'))


@pytest.fixture
def pos5(parser):
    parser.add_argument('pos5', nargs=5)
    return parser


def test_pos5_1(pos5):
    with pytest.raises(_m_forwarg.InsufficientArgumentsError):
        pos5.parse_args(shlex.split(''))


def test_pos5_2(pos5):
    with pytest.raises(_m_forwarg.InsufficientArgumentsError):
        pos5.parse_args(shlex.split('foo bar abc def'))


def test_pos5_3(pos5):
    assert pos5.parse_args(shlex.split('foo bar abc def xyz')) == \
                _m_argparse.Namespace(pos5=['foo', 'bar', 'abc', 'def', 'xyz'])


def test_pos5_4(pos5):
    with pytest.raises(_m_forwarg.UnknownArgumentError):
        pos5.parse_args(shlex.split('foo bar abc def xyz qrs'))


@pytest.fixture
def optNone(parser):
    parser.add_argument('-N', '--optNone')
    return parser


def test_optNone_1(optNone):
    assert optNone.parse_args(shlex.split('')) == _m_argparse.Namespace(
                                                                optNone=None)


def test_optNone_2(optNone):
    with pytest.raises(_m_forwarg.InsufficientArgumentsError):
        optNone.parse_args(shlex.split('-N'))


def test_optNone_3(optNone):
    assert optNone.parse_args(shlex.split('-N foo')) == _m_argparse.Namespace(
                                                                optNone='foo')


def test_optNone_4(optNone):
    with pytest.raises(_m_forwarg.UnknownArgumentError):
        optNone.parse_args(shlex.split('-N foo bar'))


@pytest.fixture
def optQues(parser):
    parser.add_argument('-Q', '--optQues', nargs='?')
    return parser


def test_optQues_1(optQues):
    assert optQues.parse_args(shlex.split('')) == _m_argparse.Namespace(
                                                                optQues=None)


def test_optQues_2(optQues):
    assert optQues.parse_args(shlex.split('-Q')) == _m_argparse.Namespace(
                                                                optQues=None)


def test_optQues_3(optQues):
    assert optQues.parse_args(shlex.split('-Q foo')) == _m_argparse.Namespace(
                                                                optQues='foo')


def test_optQues_4(optQues):
    with pytest.raises(_m_forwarg.UnknownArgumentError):
        optQues.parse_args(shlex.split('-Q foo bar'))


@pytest.fixture
def optQuesC(parser):
    parser.add_argument('-C', '--optQuesC', nargs='?', const='CONST')
    return parser


def test_optQuesC_1(optQuesC):
    assert optQuesC.parse_args(shlex.split('')) == _m_argparse.Namespace(
                                                                optQuesC=None)


def test_optQuesC_2(optQuesC):
    assert optQuesC.parse_args(shlex.split('-C')) == _m_argparse.Namespace(
                                                            optQuesC='CONST')


def test_optQuesC_3(optQuesC):
    assert optQuesC.parse_args(shlex.split('-C foo')) == _m_argparse.Namespace(
                                                                optQuesC='foo')


def test_optQuesC_4(optQuesC):
    with pytest.raises(_m_forwarg.UnknownArgumentError):
        optQuesC.parse_args(shlex.split('-C foo bar'))


@pytest.fixture
def optStar(parser):
    parser.add_argument('-S', '--optStar', nargs='*')
    return parser


def test_optStar_1(optStar):
    assert optStar.parse_args(shlex.split('')) == _m_argparse.Namespace(
                                                                optStar=None)


def test_optStar_2(optStar):
    assert optStar.parse_args(shlex.split('-S')) == _m_argparse.Namespace(
                                                                    optStar=[])


def test_optStar_3(optStar):
    assert optStar.parse_args(shlex.split('-S foo')) == _m_argparse.Namespace(
                                                            optStar=['foo'])


def test_optStar_4(optStar):
    assert optStar.parse_args(shlex.split('-S foo bar xyz abc')) == \
                    _m_argparse.Namespace(optStar=['foo', 'bar', 'xyz', 'abc'])


@pytest.fixture
def optPlus(parser):
    parser.add_argument('-P', '--optPlus', nargs='+')
    return parser


def test_optPlus_1(optPlus):
    assert optPlus.parse_args(shlex.split('')) == _m_argparse.Namespace(
                                                                optPlus=None)


def test_optPlus_2(optPlus):
    with pytest.raises(_m_forwarg.InsufficientArgumentsError):
        optPlus.parse_args(shlex.split('-P'))


def test_optPlus_3(optPlus):
    assert optPlus.parse_args(shlex.split('-P foo')) == _m_argparse.Namespace(
                                                            optPlus=['foo'])


def test_optPlus_4(optPlus):
    assert optPlus.parse_args(shlex.split('-P foo bar xyz abc')) == \
                    _m_argparse.Namespace(optPlus=['foo', 'bar', 'xyz', 'abc'])


@pytest.fixture
def optRema(parser):
    parser.add_argument('-R', '--optRema', nargs=_m_forwarg.REMAINDER)
    return parser


def test_optRema_1(optRema):
    assert optRema.parse_args(shlex.split('')) == _m_argparse.Namespace(
                                                                optRema=None)


def test_optRema_2(optRema):
    with pytest.raises(_m_forwarg.InsufficientArgumentsError):
        optRema.parse_args(shlex.split('-R'))


def test_optRema_3(optRema):
    assert optRema.parse_args(shlex.split('-R foo')) == _m_argparse.Namespace(
                                                            optRema=['foo'])


def test_optRema_4(optRema):
    assert optRema.parse_args(shlex.split('-R foo bar xyz abc')) == \
                    _m_argparse.Namespace(optRema=['foo', 'bar', 'xyz', 'abc'])


@pytest.fixture
def opt0(parser):
    parser.add_argument('-0', '--opt0', nargs=0)
    return parser


def test_opt0_1(opt0):
    assert opt0.parse_args(shlex.split('')) == _m_argparse.Namespace(opt0=None)


def test_opt0_2(opt0):
    assert opt0.parse_args(shlex.split('-0')) == _m_argparse.Namespace(opt0=[])


def test_opt0_3(opt0):
    with pytest.raises(_m_forwarg.UnknownArgumentError):
        opt0.parse_args(shlex.split('-0 foo'))


@pytest.fixture
def opt1(parser):
    parser.add_argument('-1', '--opt1', nargs=1)
    return parser


def test_opt1_1(opt1):
    assert opt1.parse_args(shlex.split('')) == _m_argparse.Namespace(opt1=None)


def test_opt1_2(opt1):
    with pytest.raises(_m_forwarg.InsufficientArgumentsError):
        opt1.parse_args(shlex.split('-1'))


def test_opt1_3(opt1):
    assert opt1.parse_args(shlex.split('-1 foo')) == _m_argparse.Namespace(
                                                                opt1=['foo'])


def test_opt1_4(opt1):
    with pytest.raises(_m_forwarg.UnknownArgumentError):
        opt1.parse_args(shlex.split('-1 foo bar'))


@pytest.fixture
def opt2(parser):
    parser.add_argument('-2', '--opt2', nargs=2)
    return parser


def test_opt2_1(opt2):
    assert opt2.parse_args(shlex.split('')) == _m_argparse.Namespace(opt2=None)


def test_opt2_2(opt2):
    with pytest.raises(_m_forwarg.InsufficientArgumentsError):
        opt2.parse_args(shlex.split('-2'))


def test_opt2_3(opt2):
    with pytest.raises(_m_forwarg.InsufficientArgumentsError):
        opt2.parse_args(shlex.split('-2 foo'))


def test_opt2_4(opt2):
    assert opt2.parse_args(shlex.split('-2 foo bar')) == _m_argparse.Namespace(
                                                        opt2=['foo', 'bar'])


def test_opt2_5(opt2):
    with pytest.raises(_m_forwarg.UnknownArgumentError):
        opt2.parse_args(shlex.split('-2 foo bar xyz'))


@pytest.fixture
def opt5(parser):
    parser.add_argument('-5', '--opt5', nargs=5)
    return parser


def test_opt5_1(opt5):
    assert opt5.parse_args(shlex.split('')) == _m_argparse.Namespace(opt5=None)


def test_opt5_2(opt5):
    with pytest.raises(_m_forwarg.InsufficientArgumentsError):
        opt5.parse_args(shlex.split('-5'))


def test_opt5_3(opt5):
    with pytest.raises(_m_forwarg.InsufficientArgumentsError):
        opt5.parse_args(shlex.split('-5 foo bar xyz abc'))


def test_opt5_4(opt5):
    assert opt5.parse_args(shlex.split('-5 foo bar xyz abc def')) == \
                _m_argparse.Namespace(opt5=['foo', 'bar', 'xyz', 'abc', 'def'])


def test_opt5_5(opt5):
    with pytest.raises(_m_forwarg.UnknownArgumentError):
        opt5.parse_args(shlex.split('-5 foo bar xyz abc def ghi'))


@pytest.fixture
def complex(parser):
    # TODO
    parser.add_argument('posNone')
    parser.add_argument('posQues', nargs='?')
    parser.add_argument('posQuesC', nargs='?', const='CONST')
    parser.add_argument('posStar', nargs='*')
    parser.add_argument('posPlus', nargs='+')
    parser.add_argument('posRema', nargs=_m_forwarg.REMAINDER)
    parser.add_argument('pos0', nargs=0)
    parser.add_argument('pos1', nargs=1)
    parser.add_argument('pos2', nargs=2)
    parser.add_argument('pos5', nargs=5)
    parser.add_argument('-N', '--optNone')
    parser.add_argument('-Q', '--optQues', nargs='?')
    parser.add_argument('-C', '--optQuesC', nargs='?', const='CONST')
    parser.add_argument('-S', '--optStar', nargs='*')
    parser.add_argument('-P', '--optPlus', nargs='+')
    parser.add_argument('-R', '--optRema', nargs=_m_forwarg.REMAINDER)
    parser.add_argument('-0', '--opt0', nargs=0)
    parser.add_argument('-1', '--opt1', nargs=1)
    parser.add_argument('-2', '--opt2', nargs=2)
    parser.add_argument('-5', '--opt5', nargs=5)
    return parser
