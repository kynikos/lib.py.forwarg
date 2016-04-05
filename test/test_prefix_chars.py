import pytest
import shlex

from . import forwarg as _m_forwarg
import argparse as _m_argparse


# TODO: Compare all the results with argparse (they must behave the same)
#@pytest.fixture(params = [_m_argparse, _m_forwarg])
@pytest.fixture(params=[_m_forwarg])
def parser(request):
    parser = request.param.ArgumentParser(prefix_chars='+')
    parser.add_argument('+O', action='store_false')
    parser.add_argument('+P', action='store_true')
    return parser


def test1(parser):
    assert parser.parse_args(shlex.split('+O +P')) == _m_argparse.Namespace(
                                                            O=False, P=True)

# TODO: Add more tests...
#       Note that mixing different prefix characters is not fully supported
#       yet, in fact the options are stored in the parser object without the
#       prefix
