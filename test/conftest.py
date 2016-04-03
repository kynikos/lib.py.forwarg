import pytest

from . import forwarg as _m_forwarg
import argparse as _m_argparse


# TODO: The different parsers must be passed as parameters to the fixture!!!
#       Everything is simplified that way, because all the tests don't have
#       to loop through the parsers
@pytest.fixture
def parsers():
    # TODO: Compare all the results with argparse (they must behave
    #       the same); in particular, reproduce all the examples in argparse's
    #       doc page

    # APparser = _m_argparse.ArgumentParser()
    FWparser = _m_forwarg.ArgumentParser()

    # return (APparser, FWparser)
    return (FWparser, )
