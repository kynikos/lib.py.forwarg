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
