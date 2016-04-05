import pytest

from . import forwarg as _m_forwarg
import argparse as _m_argparse


# TODO: Compare all the results with argparse (they must behave
#       the same); in particular, reproduce all the examples in argparse's
#       doc page
#@pytest.fixture(params = [_m_argparse, _m_forwarg])
@pytest.fixture(params=[_m_forwarg])
def parser(request):
    return request.param.ArgumentParser()
