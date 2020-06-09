# Licensed under a 3-clause BSD style license - see LICENSE.rst

import ska_helpers
__version__ = ska_helpers.get_version('Ska.quatutil')

from .quatutil import *  # noqa


def test(*args, **kwargs):
    '''
    Run py.test unit tests.
    '''
    import testr
    return testr.test(*args, **kwargs)
